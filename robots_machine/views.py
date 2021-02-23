from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from robots_machine.models import *
from robots_machine.forms import CreateRobot, RescanRobotMachineForm
from robots_machine.helpers import (
    get_robots,
    admin_robot_changes,
    delete_robot_config,
    get_rescan_robots,
    admin_robot_rescanning,
    delete_robot_rescan_definition,
    get_robot_units,
    get_robot_data,
    get_active_robots,
    get_warning_robots,
    get_alarm_robots,
    get_non_active_general,
    get_export_data)
import csv
import pytz
import json
import datetime
from io import StringIO
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext as _

@login_required
def get_robot_list(request):
    import json
    data = get_robots(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def create_robot(request):
    form = CreateRobot(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateRobot()
    return render(request, "robot_machine/add_new_robot.html", {"form": form})


@login_required
def edit_robot(request, id):
    if request.method == 'POST':
        edit_form = CreateRobot(request.POST, instance=Robots.objects.get(id=id))
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect('/settings/')
    else:
        edit_form = CreateRobot(instance=Robots.objects.get(id=id))
    return render(request, "robot_machine/edit_robot_machine.html", {"form": edit_form})


@login_required
def create_robot_rescan(request):
    form = RescanRobotMachineForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = RescanRobotMachineForm()
    return render(request, "robot_machine/add_rescan_robot_machine.html", {"form": form})


@login_required
def rescan_robot_data(request):
    data = get_rescan_robots(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def robot_monitoring(request, id):
    robot = Robots.objects.get(id=id)
    return render(request, "administration/monitoring.html", {"robot": robot})


@login_required
def robot_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = delete_robot_config(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
def robot_rescan_delete(request):
    id = request.POST.get('id', 0)
    if id:
        error = delete_robot_rescan_definition(id, request.user)
        return HttpResponse(error)
    else:
        return HttpResponse("No id sent")


@login_required
def robot_status(request):
    request_post = request.POST
    request_user = request.user

    if admin_robot_changes(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


@login_required
def robot_rescanning_status(request):
    request_post = request.POST
    request_user = request.user

    if admin_robot_rescanning(request_post, request_user):
        return HttpResponse(1)
    else:
        return HttpResponse(0)


def robot_working_progress(request, id, limiter=None):
    if not limiter:
        limiter = 24
    this_hour = timezone.now()
    history_limiter = this_hour - timezone.timedelta(hours=int(8000))
    end = timezone.now()
    chart_data = get_robot_data(robot_id=id, end=end, start=history_limiter)
    s = StringIO()
    json.dump(chart_data, s)
    s.seek(0)

    return HttpResponse(s.read())


def robot_working_progress_delta(request, id, delta):
    end = timezone.now()
    delta = int(delta)
    delta = datetime.datetime.fromtimestamp(delta/1000.0)
    chart_data = get_robot_data(robot_id=id, end=end, start=delta.replace(tzinfo=pytz.UTC))
    s = StringIO()
    json.dump(chart_data, s)
    s.seek(0)
    return HttpResponse(s.read())


def administration_dashboard(request, id, limiter=None):
    """
    This function return data for d3.js robot pie chart and robot table, based on date filter!
    :param request: request
    :param id: robot_id
    :param limiter: date filter (yesterday, last 7 days, last month, etc...)
    :return: data for robot dashboard (dictionary)

    OEE calculation:
        a)
            OEE = (Good Count × Ideal Cycle Time) / Planned Production Time
            Ideal Cycle Time - theoretical minimum part to produce one part
            Planned Production Time - total time that equipment is excepted to produce (420 minutes × 60 seconds)
        b)
            Availability = Run Time / Planned Production Time
            Run Time = Planned Production Time − Stop Time

        c)
            Performance = (Ideal Cycle Time × Total Count) / Run Time
            Performance = (Total Count / Run Time) / Ideal Run Rate

        d)
            Quality = Good Count / Total Count


    """
    if not limiter:
        limiter = 24

    robots_status = Robots.objects.filter(id=id)
    if robots_status.exists():
        robot = robots_status.first()
        robot_working_exist = RobotWorkingProgress.objects.filter(robot_id=id)
        if robot_working_exist.exists():
            robot_last_updated_record = RobotWorkingProgress.objects.filter(robot_id=id).latest('updated').updated

            # running status
            check_time = timezone.now() - timezone.timedelta(minutes=15)
            running_status = False
            if check_time < robot_last_updated_record:
                running_status = True

            # get initial robot working data
            now = timezone.now()
            history_limiter = now - timezone.timedelta(hours=int(limiter))
            robot_units, robot_filter, working_days, chart_data = get_robot_units(
                robot_id=id, end=now, start=history_limiter)

            # total working minutes
            total_working_minutes = 0
            for x in working_days:
                for k, v in x.items():
                    total_working_minutes += v

            # get oee variables
            ideal_cycle_time = robot.ideal_cycle_second
            good_units = robot_units['produced_units'] if robot_units['produced_units'] else 0
            total_count = robot_units['good_intensity'] if robot_units['good_intensity'] else 0
            planned_production_time = robot.planned_production_min
            stop_time = planned_production_time - total_working_minutes
            run_time = planned_production_time - stop_time
            # Calculate Availability
            if planned_production_time > 0:
                availability = run_time / planned_production_time
            else:
                availability = 0

            # Calculate Performance
            if total_count > 0 and run_time > 0:
                run_time_second = run_time * 60
                performance = ideal_cycle_time * total_count / run_time_second
            else:
                performance = 0

            # Calculate Quality
            if good_units > 0 and total_count > 0:
                quality = good_units / total_count
            else:
                quality = 0

            # Calculate Total OEE

            # Checking result
            oee_final = availability * performance * quality
            oee_final = oee_final * 100
            if oee_final > 100:
                oee_final = 0

            availability = availability * 100
            if availability > 100:
                availability = 0

            performance = performance * 100
            if performance > 100:
                performance = 0

            quality = quality * 100
            if quality > 100:
                quality = 0

            rejected_units = total_count - good_units
            dashboard_data = {
                'robot_product_name': robot.product.name,
                'robot_resource': robot.serial_number,
                'running_status': running_status,
                'running_time': run_time,
                'rejected_units': rejected_units,
                'excepted_units': robot_units['excepted_units'] if robot_units['excepted_units'] else 0,
                'active_alarms': robot_units['active_alarms'] if robot_units['active_alarms'] else 0,
                'produced_units': robot_units['produced_units'] if robot_units['produced_units'] else 0,
                'good_units': good_units,
                'robot_id': id,
                'planned_production_time': planned_production_time,
                'oee_final': round(oee_final, 3),
                'availability': round(availability, 3),
                'performance': round(performance, 3),
                'quality': round(quality, 3),
                'time_delta': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            return render("robot_machine/robot_dashboard.html", {"dashboard_data": dashboard_data})

    dashboard_data = {
        'robot_product_name': "",
        'robot_resource': "",
        'running_status': "",
        'excepted_units': 0,
        'active_alarms': 0,
        'produced_units': 0,
        'good_units': 0,
        'planned_production_time': 4,
        'rejected_units': 0,
        'robot_id': id,
        'oee_final': 0,
        'availability': 0,
        'performance': 0,
        'quality': 0,
        'running_time': 0,
        'time_delta': timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return render("robot_machine/robot_dashboard.html", {"dashboard_data": dashboard_data})


# API OEE pie charts


class OeeChart(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, id, format=None):
        robots_status = Robots.objects.filter(id=id).exists()
        if robots_status:
            robot_working_exist = RobotWorkingProgress.objects.filter(robot_id=id).exists()
            if robot_working_exist:
                robot_units = get_robot_units(robot_id=id)
                # OEE = (Good Count × Ideal Cycle Time) / Planned Production Time
                # Good Count - good_units
                # Ideal Cycle Time - theoretical minimum part to produce one part
                # Planned Production Time - total time that equipment is excepted to produce (420 minutes × 60 seconds)

                good_units = robot_units['good_units'] if robot_units['good_units'] else 0
                ideal_cycle_time = 1
                planned_production_time = 25200
                oee_units = int(good_units) * ideal_cycle_time
                oee = oee_units / planned_production_time
                oee_final = oee * 100
                return HttpResponse(oee_final)


class AvailabilityChart(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, id, format=None):
        robots_status = Robots.objects.filter(id=id).exists()
        if robots_status:
            robot_working_exist = RobotWorkingProgress.objects.filter(robot_id=id).exists()
            if robot_working_exist:
                robot_units = get_robot_units(robot_id=id)
                # Availability = Run Time / Planned Production Time
                # Run Time = Planned Production Time − Stop Time
                planned_production_time = robot_units['planned_production_time'] if robot_units['planned_production_time'] else 0
                down_time = robot_units['down_time'] if robot_units['down_time'] else 0

                if planned_production_time > 0 and down_time > 0:
                    run_time = planned_production_time - down_time
                    availability = run_time / planned_production_time
                else:
                    availability = 0

                return HttpResponse(availability)


class PerformanceChart(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, id, format=None):
        robots_status = Robots.objects.filter(id=id).exists()
        if robots_status:
            robot_working_exist = RobotWorkingProgress.objects.filter(robot_id=id).exists()
            if robot_working_exist:
                robot_units = get_robot_units(robot_id=id)

                # Performance = (Ideal Cycle Time × Total Count) / Run Time
                # Performance = (Total Count / Run Time) / Ideal Run Rate
                ideal_cycle_time = robot_units['ideal_cycle_time'] if robot_units['ideal_cycle_time'] else 0
                total_count = robot_units['total_count'] if robot_units['total_count'] else 0
                planned_production_time = robot_units['planned_production_time'] if robot_units['planned_production_time'] else 0
                down_time = robot_units['down_time'] if robot_units['down_time'] else 0

                if ideal_cycle_time > 0 and total_count > 0:
                    run_time = planned_production_time - down_time
                    performance = ideal_cycle_time * total_count / run_time
                else:
                    performance = 0

                return HttpResponse(performance)


class QualityChart(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, id, format=None):
        robots_status = Robots.objects.filter(id=id).exists()
        if robots_status:
            robot_working_exist = RobotWorkingProgress.objects.filter(robot_id=id).exists()
            if robot_working_exist:
                robot_units = get_robot_units(robot_id=id)

                # Quality = Good Count / Total Count

                good_count = robot_units['good_units'] if robot_units['good_units'] else 0
                total_count = robot_units['total_count'] if robot_units['total_count'] else 0

                if good_count > 0 and total_count > 0:
                    quality = good_count / total_count
                else:
                    quality = 0

                return HttpResponse(quality)


@login_required
def get_active_robot_list(request):
    data = get_active_robots(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def get_warning_robot_list(request):
    data = get_warning_robots(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def get_alarm_robot_list(request):
    data = get_alarm_robots(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def get_not_active_robot(request):
    data = get_non_active_general(request.user)
    response = {"data": data}
    s = StringIO()
    json.dump(response, s)
    s.seek(0)

    return HttpResponse(s.read())


@login_required
def robot_export_report(request):
    filters = request.POST.dict()
    response = HttpResponse(content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=robot_data_report.csv'

    filters = {
        'start': filters['start'],
        'end': filters['end'],
        'datetime_range': filters['datetimerange'],
        'start_time': filters['start_time'],
        'end_time': filters['end_time'],
        'company': filters['company'],
        'city': filters['city'],
        'robot_status_filter': filters['robot_status_mode']
    }

    export_data = get_export_data(filters=filters)
    writer = csv.writer(response)
    writer.writerow([item for item in ['timestamp', 'active alarms', 'robot name', 'excepted units', 'good units',
                                       'produced units', 'rejected units', 'big errors type1', 'big errors type2',
                                       'errors', 'errors max type1', 'errors max type2', 'good intensity', 'intensity',
                                       'intensity_max', 'max_errors', 'serial_number', 'enabled', 'city',
                                       'robot_ip_address', 'created', 'planned_production_hour', 'ideal_cycle_second']
                     ])

    for item in export_data:
        print(item)
        writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                         item[10], item[11], item[12], item[13], item[14], item[15], item[16], item[17], item[18],
                         item[19], item[20], item[21], item[22]])
    return response


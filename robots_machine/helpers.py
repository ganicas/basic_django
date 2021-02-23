import random
from collections import defaultdict
from administration.models import RescanRobotMachine
from robots_machine.models import Robots, RobotWorkingProgress
from datetime import date
from django.db.models import Count, Sum, Q, When, Value
from django.utils import timezone

def get_robots(robot):
    robot_list = []
    results = Robots.objects.all()
    name_link = u'<a href="{2}/edit/robot/{0}/">{1}</a>'
    robot_graph = u'<a href="{2}/robot/dashboard/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            row.append(name_link.format(result.id, result.name, ''))
            row.append(robot_graph.format(result.id, result.name+str(' monitoring'), ''))
            row.append(result.serial_number)
            row.append(result.city)
            row.append(result.robot_ip_address)
            row.append(result.robot_username)
            row.append(result.robot_password)
            if result.product:
                row.append(result.product.name)
            else:
                row.append("There is no robot added yet!")

            if result.company:
                row.append(result.company.name)
            else:
                row.append("There is no robot added yet!")

            if result.active:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            robot_list.append(row)
        except Exception as e:
            print(e)
    return robot_list


def admin_robot_changes(request_post, request_user):
    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = Robots.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.set_bool('active', True)
                result.save()
            elif request_dict['name'] == 'disable':
                result.set_bool('active', False)
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def admin_robot_rescanning(request_post, request_user):
    try:
        request_dict = dict()
        for key in request_post:
            request_dict[key] = request_post[key]

        results = RescanRobotMachine.objects.filter(id=request_dict['id'])
        for result in results:
            if request_dict['name'] == 'enable':
                result.activate_rescan = True
                result.save()
            elif request_dict['name'] == 'disable':
                result.activate_rescan = False
                result.save()
            elif request_dict['name'] == 'delete':
                result.delete()

        return True
    except Exception as e:
        print(e)
        return False


def delete_robot_config(id, user):

    try:
        robot = Robots.objects.get(id=id)
        rescan_robot_delete = RescanRobotMachine.objects.filter(robot_id=id)
        if rescan_robot_delete.exists():
            rescan_robot_delete.delete()
        robot_working_progres = RobotWorkingProgress.objects.filter(robot_id=id)
        if robot_working_progres.exists():
            robot_working_progres.delete()

    except Robots.DoesNotExist:
        return u"Robot doesn't exist!"

    if robot.active:
        return u"Robot is enabled!"

    robot.delete()

    return 1


def delete_robot_rescan_definition(id, user):

    try:
        rescan_robot = RescanRobotMachine.objects.get(id=id)

    except RescanRobotMachine.DoesNotExist:
        return u"Robot rescan doesn't exist!"

    if rescan_robot.activate_rescan:
        return u"Robot rescan is enabled!"

    rescan_robot.delete()

    return 1


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def get_rescan_robots(robot):
    rescan_robot_list = []
    results = RescanRobotMachine.objects.all()
    name_link = u'<a class="denied_link" href="{2}/edit/robot/{0}/">{1}</a>'
    button_on = u'<button type="button" id ="btn" class="btn btn-success" name="{0}"><i>Enabled</i></button>'
    button_off = u'<button type="button" class="btn btn-secondary" name="{0}"><i></i>Disabled</button>'
    delete = '<a type="button" class="btn btn-danger" id="{0}" href="#"><i class="sy_remove"></i>Delete</a>'
    for result in results:
        try:
            row = list()
            if result.robot:
                row.append(name_link.format(result.robot.id, result.robot.name, ''))
            row.append(str(result.start_date))
            row.append(str(result.end_date))

            if result.rescan_status:
                row.append('<p><font color="green">rescan</p>')
            else:
                row.append('<p><font color="orange">not rescan</p>')

            if result.note:
                row.append(result.note)
            else:
                if result.activate_rescan:
                    row.append('<p><font color="red">robot rescanning in progress</p>')
                else:
                    row.append('<p><font color="blue">robot rescanning deactivated</p>')

            if result.activate_rescan:
                row.append(button_on.format(result.id))
            else:
                row.append(button_off.format(result.id))
            row.append(delete.format(result.id))
            rescan_robot_list.append(row)
        except Exception as e:
            print(e)
    return rescan_robot_list


def get_robot_units(robot_id, start, end):
    robot_filter = RobotWorkingProgress.objects.filter(robot_id=robot_id, updated__range=(start, end))
    from django.db import connection
    aggregation_data = robot_filter.order_by('updated').aggregate(
        excepted_units=Sum('excepted_units'),
        active_alarms=Sum('active_alarms'),
        produced_units=Sum('produced_units'),
        good_units=Sum('good_units'),
        rejected_units=Sum('rejected_units'),
        good_intensity=Sum('good_intensity'),

    )
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    end = end.strftime('%Y-%m-%d %H:%M:%S')

    query = """ select
                to_char(robot_datetime, 'YYYY-MM-DD HH24:MI:') AS "timestamp",
                count(*)
                from robot_working_progress
                where robot_id = {}
                and updated BETWEEN '{}' and '{}'
                group by timestamp;""".format(robot_id, start, end)

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    working_days = defaultdict(list)
    chart_data = []
    for x in result:
        working_day_string = x[0].split()
        day = working_day_string[0]
        minute = working_day_string[1][:-1]
        robot_data = list(x)
        chart_data.append({robot_data[0][:-1]: robot_data[1]})
        working_days[day].append(minute)
    working_data = calculate_working_hours(working_days)
    return aggregation_data, robot_filter, working_data, chart_data


def calculate_working_hours(real_working_progress):
    working_data = []
    for k, v in real_working_progress.items():
        real_working_minute = 0
        for x in v:
            real_working_minute += 1
        working_hours_per_day = {k: real_working_minute}
        working_data.append(working_hours_per_day)
    return working_data


def get_robot_data(robot_id, start, end):
    from django.db import connection
    start = start.strftime('%Y-%m-%d %H:%M:%S')
    end = end.strftime('%Y-%m-%d %H:%M:%S')
    query = """ select
                to_char(robot_datetime, 'YYYY-MM-DD HH24:MI TZ') AS "timestamp",
                count(*)
                from robot_working_progress
                where robot_id = {}
                and robot_datetime BETWEEN '{}' and '{}'
                group by timestamp;""".format(robot_id, start, end)

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    chart_data = []
    for x in result:
        robot_data = list(x)
        time = robot_data[0]

        chart_data.append([time, robot_data[1]])
    if len(chart_data):
        sort_data = sort_robot_working_data(chart_data)
        return sort_data
    return []


def sort_robot_working_data(data):
    sorted_list = sorted(data, key=lambda x: x[0])
    return sorted_list


def get_active_robots(robots):
    robot_list = []
    this_hour = timezone.now()
    history_limiter = this_hour - timezone.timedelta(hours=8000)
    robot_filter = RobotWorkingProgress.objects.filter(updated__range=(history_limiter, this_hour)).distinct('robot')

    if robot_filter:
        name_link = u'<a href="{2}/edit/robot/{0}/">{1}</a>'
        robot_graph = u'<a href="{2}/robot/dashboard/{0}/">{1}</a>'
        for result in robot_filter:
            try:
                row = list()
                row.append(name_link.format(result.robot.id, result.robot.name, ''))
                row.append(robot_graph.format(result.robot.id, result.robot.name+str(' monitoring'), ''))
                row.append(result.robot.serial_number)
                row.append(result.robot.city)
                row.append(result.robot.robot_ip_address)
                robot_list.append(row)
            except Exception as e:
                print(e)
    return robot_list


def get_warning_robots(robots):
    robot_list = []
    this_hour = timezone.now()
    history_limiter = this_hour - timezone.timedelta(hours=8000)
    robot_filter = RobotWorkingProgress.objects.filter(updated__range=(history_limiter, this_hour)).distinct('robot')

    if robot_filter:
        name_link = u'<a href="{2}/edit/robot/{0}/">{1}</a>'
        robot_graph = u'<a href="{2}/robot/dashboard/{0}/">{1}</a>'
        for result in robot_filter:
            try:
                row = list()
                row.append(name_link.format(result.robot.id, result.robot.name, ''))
                row.append(robot_graph.format(result.robot.id, result.robot.name+str(' monitoring'), ''))
                row.append(result.robot.serial_number)
                row.append(result.robot.city)
                row.append(result.robot.robot_ip_address)
                robot_list.append(row)
            except Exception as e:
                print(e)
    return robot_list


def get_alarm_robots(robots):
    robot_list = []
    this_hour = timezone.now()
    history_limiter = this_hour - timezone.timedelta(hours=8000)
    robot_filter = RobotWorkingProgress.objects.filter(updated__range=(history_limiter, this_hour)).distinct('robot')

    if robot_filter:
        name_link = u'<a href="{2}/edit/robot/{0}/">{1}</a>'
        robot_graph = u'<a href="{2}/robot/dashboard/{0}/">{1}</a>'
        for result in robot_filter:
            try:
                row = list()
                row.append(name_link.format(result.robot.id, result.robot.name, ''))
                row.append(robot_graph.format(result.robot.id, result.robot.name+str(' monitoring'), ''))
                row.append(result.robot.serial_number)
                row.append(result.robot.city)
                row.append(result.robot.robot_ip_address)
                robot_list.append(row)
            except Exception as e:
                print(e)
    return robot_list


def get_non_active_general(robots):
    robot_list = []
    this_hour = timezone.now()
    history_limiter = this_hour - timezone.timedelta(hours=8000)
    robot_filter = RobotWorkingProgress.objects.filter(updated__range=(history_limiter, this_hour)).distinct('robot')

    if robot_filter:
        name_link = u'<a href="{2}/edit/robot/{0}/">{1}</a>'
        robot_graph = u'<a href="{2}/robot/dashboard/{0}/">{1}</a>'
        for result in robot_filter:
            try:
                row = list()
                row.append(name_link.format(result.robot.id, result.robot.name, ''))
                row.append(robot_graph.format(result.robot.id, result.robot.name+str(' monitoring'), ''))
                row.append(result.robot.serial_number)
                row.append(result.robot.city)
                row.append(result.robot.robot_ip_address)
                robot_list.append(row)
            except Exception as e:
                print(e)
    return robot_list


def date_format(date_string, time_string):
    split_date = date_string.split('.')
    year = split_date[2]
    date = split_date[1]
    day = split_date[0]
    date_string = str(year)+str('-')+str(date)+str('-')+str(day)+str(" ")+str(time_string)

    return date_string


def get_export_data(filters):
    start_date = filters['start']
    end_date = filters['end']
    start_time = filters['start_time']
    end_time = filters['end_time']

    # format star and end date
    start = date_format(start_date, start_time)
    end = date_format(end_date, end_time)
    from django.db import connection
    query = """ select
                to_char(robot_datetime, 'YYYY-MM-DD HH24:MI') AS "timestamp",
                robot_working_progress.active_alarms,
                robots_machine.name,
                robot_working_progress.excepted_units, 
                robot_working_progress.good_units,
                robot_working_progress.produced_units, 
                robot_working_progress.rejected_units,
                robot_working_progress.big_errors_type1,
                robot_working_progress.big_errors_type2,
                robot_working_progress.errors,
                robot_working_progress.errors_max_type1,
                robot_working_progress.errors_max_type2,
                robot_working_progress.good_intensity,
                robot_working_progress.intensity,
                robot_working_progress.intensity_max,
                robot_working_progress.max_errors,
                robots_machine.serial_number,
                robots_machine.enabled,
                robots_machine.city,
                robots_machine.robot_ip_address,
                robots_machine.created,
                robots_machine.planned_production_hour,
                robots_machine.ideal_cycle_second
                
                from robot_working_progress
                left join robots_machine
                on robot_working_progress.robot_id = robots_machine.id
                where robot_working_progress.updated BETWEEN '{}' and '{}'
                """.format(start, end)

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()

    return result

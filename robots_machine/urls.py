from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^robot/create/$', views.create_robot, name='create_robot'),
    url(r'^robot/list/$', views.get_robot_list, name='robot_list'),
    url(r'^rescan/robot/data/$', views.rescan_robot_data, name='rescan_robot_data'),
    url(r'^edit/robot/(?P<id>\d+)/?$', views.edit_robot, name='edit_robot'),
    url(r'^create/robot/rescan/', views.create_robot_rescan, name='edit_robot_rescan'),
    url(r'^robot/monitoring/(?P<id>\d+)/?$', views.robot_monitoring, name='robot_monitoring'),
    url(r'^service/robot_status/$', views.robot_status),
    url(r'^delete/robots/$', views.robot_delete),
    url(r'^delete/robots/rescan/$', views.robot_rescan_delete),
    url(r'^service/robot_status/rescanning/$', views.robot_rescanning_status),
    url(r'^robot/dashboard/(?P<id>\d+)/?(?P<limiter>\w+|)/$', views.administration_dashboard, name='administration_dashboard'),
    url(r'^robot/dashboard/line/chart/(?P<id>\d+)/?(?P<limiter>\w+|)/$', views.robot_working_progress, name='robot_working_progress'),
    url(r'^robot/dashboard/line/chart/delta/(?P<id>\d+)/?(?P<delta>\w+|)/$', views.robot_working_progress_delta, name='robot_working_progress_delta'),

    # REST API for robot OEE charts
    url(r'^oee_chart/(?P<id>\d+)/?$', views.OeeChart.as_view(), name='oee_chart'),
    url(r'^availability_chart/(?P<id>\d+)/?$', views.AvailabilityChart.as_view(), name='availability_chart'),
    url(r'^performance_chart/(?P<id>\d+)/?$', views.PerformanceChart.as_view(), name='performance_chart'),
    url(r'^quality_chart/(?P<id>\d+)/?$', views.QualityChart.as_view(), name='quality_chart'),

    url(r'^api/active/robot/', views.get_active_robot_list, name='get_active_robot_list'),
    url(r'^api/warning/robot/', views.get_warning_robot_list, name='get_warning_robot_list'),
    url(r'^api/alarm/robot/', views.get_alarm_robot_list, name='get_alarm_robot_list'),
    url(r'^api/general/not/active/robot/', views.get_not_active_robot, name='get_not_active_robot'),
    url(r'^api/report/service/download_robot_list_report/?$', views.robot_export_report, name='robot_export_report'),

]
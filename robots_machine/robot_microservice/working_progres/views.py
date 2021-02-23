from datetime import datetime

from robots_machine.models import Robots, RobotWorkingProgress

from administration.common.logging.setup import logger


class RobotMicroServiceDataHandler(object):
    def __init__(self, robot_data):
        self.robot_data = robot_data

    def handle_robot_working_progress(self):
        full_data = self.robot_data['data']
        working_progress_list = []
        for element in full_data:
            robot_time = datetime.strptime(element['datetime'], '%Y/%m/%d %H:%M:%S.%f')
            robot_good_working_units = element['ok_type1']
            robot_id = self.robot_data['robot_id']
            intensity_max = element['max_intensity']
            errors = element['errors']
            max_errors = element['max_errors']
            big_errors_type1 = element['big_errors_type_1']
            big_errors_type2 = element['big_errors_type_2']
            errors_max_type1 = element['errors_type_1']
            errors_max_type2 = element['errors_type_2']
            intensity = element['intensity']
            good_intensity = element['ok_intensity']
            try:
                robot = Robots.objects.get(id=robot_id)
            except Robots.DoesNotExist:
                logger.error("Robot doesn't exists {}".format(robot_id))
                continue
            working_progress_item = RobotWorkingProgress(
                robot=robot,
                robot_datetime=robot_time,
                produced_units=int(robot_good_working_units),
                good_intensity=good_intensity,
                errors_max_type2=errors_max_type2,
                errors_max_type1=errors_max_type1,
                big_errors_type2=big_errors_type2,
                big_errors_type1=big_errors_type1,
                max_errors=max_errors,
                errors=errors,
                intensity_max=intensity_max,
                intensity=intensity
            )
            working_progress_list.append(working_progress_item)
        RobotWorkingProgress.objects.bulk_create(working_progress_list)



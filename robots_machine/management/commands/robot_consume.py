
from robots_machine.tasks import run_kombu_process
from utils.commands import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            run_kombu_process()
        except (KeyboardInterrupt, Exception) as e:
            print(e)

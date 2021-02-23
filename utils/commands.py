import inspect
import logging
import os
import sys
import traceback
from uuid import uuid4

from django_nameko import get_pool
from django.core.management.base import BaseCommand as DjangoBaseCommand
from django.conf import settings
from django.utils import timezone

from administration.common.logging.setup import logger
from main import send_mail


class JobStats:
    @classmethod
    def _execute(cls, method, *args, **kwargs):
        if not settings.USE_JOBSTATS_RPC:
            return

        with get_pool().next() as rpc:
            service = rpc.job_stats_rpc
            getattr(service, method).call_async(*args, **kwargs)

    @classmethod
    def start(cls, title, source, job_key, tags=None):
        uuid = uuid4().hex

        if tags is None:
            tags = []

        tags = [str(t) for t in tags]

        rpc_call_data = {
            "uuid": uuid,
            "title": title,
            "source": source,
            "job_key": job_key,
            "tags": tags,
        }
        cls._execute('start', rpc_call_data)

        return uuid

    @classmethod
    def stop(cls, uuid, finished_ok=True):
        cls._execute('stop', uuid, finished_ok)

    @classmethod
    def set_counter(cls, uuid, key, value):
        cls._execute('set_counter', uuid, key, value)

    @classmethod
    def increment_by(cls, uuid, key, value):
        cls._execute('increment_by', uuid, key, value)

    @classmethod
    def decrement_by(cls, uuid, key, value):
        cls._execute('decrement_by', uuid, key, value)

    @classmethod
    def append(cls, uuid, key, values):
        cls._execute('append', uuid, key=key, values=values)

    @classmethod
    def add_tags(cls, uuid, *tags_to_add):
        cls._execute('add_tags', uuid, tags=tags_to_add)


class BaseCommand(DjangoBaseCommand):

    def _on_command_done(self):
        pass

    @property
    def job_title(self):
        return ' '.join(self._get_script_name().split('_')).capitalize()

    @property
    def job_source(self):
        return settings.SERVER_ID

    @property
    def job_key(self):
        return self._get_script_name()

    @property
    def job_tags(self):
        return []

    @classmethod
    def _get_company_tag(cls, company_id):
        return '__company{}__'.format(company_id)

    def _get_script_name(self):
        try:
            filepath = sys.modules[self.__class__.__module__].__file__
            return os.path.splitext(os.path.basename(filepath))[0]
        except:
            return 'unknown'

    def _send_exception_mail(self):
        command_filepath = inspect.getfile(self.__class__)
        command_name = os.path.splitext(os.path.basename(command_filepath))[0]

        subject_format = "[Management command error] Error while executing {} command at {}"
        subject = subject_format.format(command_name, timezone.now())
        message = "Command params: {}\n\n{}".format(self.options, traceback.format_exc())

        send_mail(
            to=[settings.DEV_MAILING_LIST],
            subject=subject,
            body=message,
            fail_silently=True,
        )

    def _on_exception(self, e, message):
        logger.exception(
            "Got exception while executing {} command with params: {}"
            .format(__file__, self.options)
        )
        JobStats.append(self.process_uid, 'System errors', [message])

        if not settings.DEBUG:
            self._send_exception_mail()
        raise e

    def execute(self, *args, **options):
        self.options = options

        self.process_uid = JobStats.start(
            title=self.job_title,
            source=self.job_source,
            job_key=self.job_key,
            tags=self.job_tags,
        )

        finished_ok = False

        try:
            self.handle(*args, **options)
            finished_ok = True

        except KeyboardInterrupt as e:
            self._on_exception(e, 'KeyboardInterrupt')

        except Exception as e:
            self._on_exception(e, str(e))

        finally:
            JobStats.stop(self.process_uid, finished_ok=finished_ok)
            self._on_command_done()

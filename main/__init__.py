import csv
import re
import json
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from django.db.models import F, Prefetch

def send_mail(to, subject, body, is_html=False, from_email=settings.DEFAULT_FROM_EMAIL, reply_to="",
              attachment=None, fail_silently=False, multiple_attachments=None,
              force_send=False, logger=None):

    def send_email_data(to, body, multiple_attachments, attachment, is_html):
        if not is_html:
            body += "\n\n-- \n" + settings.SITE_URL

        if multiple_attachments is None:
            multiple_attachments = []

        if type(to) != list:
            to = [to]
        email = EmailMessage(subject, body, to=to)

        if is_html:
            email.content_subtype = "html"

        if attachment != None:
            (filename, content, mime) = attachment
            email.attach(filename, content, mime)

        for filename in multiple_attachments:
            email.attach_file(filename)

        try:
            res = email.send(fail_silently=fail_silently)
            if logger:
                logger.info('Mail sent with result: {}'.format(res))
            return True
        except Exception as e:
            if logger:
                logger.exception('Error sending email: {}'.format(e))
            return False

    if not settings.SEND_EMAIL:
        if not force_send:
            return
        else:
            return send_email_data(to, body, multiple_attachments, attachment, is_html)

    return send_email_data(to, body, multiple_attachments, attachment, is_html)

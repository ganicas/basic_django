from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
import json


def render_to_response(template_name, context, context_instance, **kw):
    request = context_instance.request
    if 'user' not in context:
        context['user'] = request.user
    return render(request, template_name, context)


def render_to_string(template_name, context, **kw):
    request = None
    if 'context_instance' in kw:
        request = kw['context_instance'].request
        if 'user' not in context:
            context['user'] = request.user
    template = get_template(template_name)
    return template.render(context, request=request)


def json_response(data, status_code=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status_code)


def create_redis_key(auth_user_hash, company_id, data_name):
    """Creates a redis key for the user, using auth user hash as the unique identifier."""
    result = '_'.join([auth_user_hash, str(company_id), data_name])
    return result

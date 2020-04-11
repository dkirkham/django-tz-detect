# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

from ..defaults import TZ_DETECT_SCRIPTS, TZ_DETECT_PERIOD
from ..utils import convert_header_name

import time

register = template.Library()


@register.inclusion_tag('tz_detect/detector.html', takes_context=True)
def tz_detect(context, **script_attrs):
    return {
        'show': (context.get('request').session.get('tz_detected_ts', 0) + TZ_DETECT_PERIOD) < time.time(),
        'debug': getattr(settings, 'DEBUG', False),
        'csrf_header_name': convert_header_name(
            getattr(settings, 'CSRF_HEADER_NAME', 'HTTP_X_CSRFTOKEN')
        ),
        'script_attrs': script_attrs,
        'scripts': TZ_DETECT_SCRIPTS,
    }

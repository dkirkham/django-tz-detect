# -*- coding: utf-8 -*-

import pytz
from pytz.tzinfo import BaseTzInfo

from django.utils import timezone

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    MiddlewareMixin = object


class TimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        tz = request.session.get('tz_detected')
        if tz:
            timezone.activate(pytz.timezone(tz))
        else:
            timezone.deactivate()

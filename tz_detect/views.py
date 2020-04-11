# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import View

import pytz
import time

class SetOffsetView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        tz = request.POST.get('tz', None)
        if not tz:
            return HttpResponse("No 'tz' parameter provided", status=400)

        try:
            _ = pytz.timezone(tz)
        except pytz.exceptions.UnknownTimeZoneError:
            return HttpResponse("Invalid 'tz' value provided", status=400)

        request.session['tz_detected'] = tz
        request.session['tz_detected_ts'] = time.time()

        return HttpResponse("OK")

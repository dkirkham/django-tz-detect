# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from pytz.tzinfo import BaseTzInfo

from tz_detect.templatetags.tz_detect import tz_detect
from tz_detect.utils import convert_header_name
from tz_detect.views import SetOffsetView


class ViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def add_session(self, request):
        SessionMiddleware().process_request(request)

    def test_xhr_valid(self):
        request = self.factory.post('/abc', {'tz': 'Australia/Melbourne'})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('tz_detected', request.session)
        self.assertIsInstance(request.session['tz_detected'], BaseTzInfo)
        self.assertIn('tz_detected_ts', request.session)
        self.assertIsInstance(request.session['tz_detected_ts'], float)

    def test_xhr_bad_method(self):
        request = self.factory.get('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_xhr_no_offset(self):
        request = self.factory.post('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_xhr_bad_offset(self):
        request = self.factory.post('/abc', {'tz': 'Nowhere'})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class ConvertHeaderNameTestCase(TestCase):
    """Test for `templatetags.tz_detect.convert_header_name`

    This util converts django header name to suitable for AJAX request
    """
    def test_default_header_name(self):
        # default value for settings.CSRF_HEADER_NAME
        setting = 'HTTP_X_CSRFTOKEN'
        result = convert_header_name(setting)
        self.assertEqual(result, 'x-csrftoken')

    def test_custom_header_name(self):
        setting = 'HTTP_X_XSRF_TOKEN'
        result = convert_header_name(setting)
        self.assertEqual(result, 'x-xsrf-token')

    def test_custom_header_without_http_prefix(self):
        setting = 'X_XSRF_TOKEN'
        result = convert_header_name(setting)
        self.assertEqual(result, 'x-xsrf-token')


class TemplatetagTestCase(TestCase):

    def test_no_request_context(self):
        try:
            tz_detect({})
        except KeyError as e:
            if e.message == 'request':
                self.fail("Templatetag shouldn't expect request in context.")
            else:
                raise

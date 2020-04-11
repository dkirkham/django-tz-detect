# -*- coding: utf-8 -*-

def convert_header_name(django_header):
    """Converts header name from django settings to real header name.

    For example:
    'HTTP_CUSTOM_CSRF' -> 'custom-csrf'
    """
    return django_header.lower().replace('_', '-').split('http-')[-1]

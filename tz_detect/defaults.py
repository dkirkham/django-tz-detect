# -*- coding: utf-8 -*-

from django.conf import settings

# How often to check
TZ_DETECT_PERIOD = getattr(settings, 'TZ_DETECT_PERIOD', 3*3600)

# Version of moment and moment-timezone to load
TZ_DETECT_SCRIPTS = getattr(settings, 'TZ_DETECT_SCRIPTS', [
  '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js" integrity="sha256-4iQZ6BVL4qNKlQ27TExEhBN1HFPvAvAMbFavKKosSWQ=" crossorigin="anonymous"></script>',
  '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment-timezone/0.5.28/moment-timezone-with-data-10-year-range.min.js" integrity="sha256-HS6OzSyhM0rDG0PhZGwf/FvptBzIJnv4MgL2pe87xgg=" crossorigin="anonymous"></script>'
])
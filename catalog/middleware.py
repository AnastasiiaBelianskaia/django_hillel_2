import logging
import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.session.save()
            tzname = request.session.get('django_timezone')
            if tzname:
                timezone.activate(zoneinfo.ZoneInfo(tzname))
            else:
                timezone.deactivate()
        except BaseException:
            logging.exception('An exception was thrown!')
        return self.get_response(request)

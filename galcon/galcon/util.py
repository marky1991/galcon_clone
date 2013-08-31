
from collections import namedtuple
from django.utils import timezone
import pytz

class cached_property:
    """A read-only @property that is only evaluated once."""
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result

class My_Timezone_Middleware:
    def process_request(self, request):
        user_timezone = None
        #if request.user.is_authenticated():
        #    user_timezone = request.session.get("current_timezone")
        if True or "timezone" not in request.session:
            try:
                user_timezone = pytz.FixedOffset(-int(request.COOKIES.get("offset")))
                #print("Getting timezone from cookies")
                request.session["timezone"] = user_timezone
            except TypeError:
                pass
        else:
            print("Getting it from the session")
            print(request.session.items(), "Session")
            user_timezone = request.session.get("timezone")
            print(user_timezone, "timezone from session")
        if user_timezone:
            timezone.activate(user_timezone)
        else:
            timezone.deactivate()

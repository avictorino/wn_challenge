import time
from django.http import JsonResponse


def measure_view(function):
    def wrap(request, *args, **kwargs):
        t = time.process_time()

        payload = function(request, *args, **kwargs)

        payload['elapsed_time'] = f"spend {round(time.process_time() - t, 3)} seconds to process"

        return JsonResponse(payload)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
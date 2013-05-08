import time
from twisted.internet.defer import maybeDeferred
from functools import wraps
from eagleeye.riemann import Riemann

class Metric:

    def __init__(self, myhost='EagleEye', timeprecision=2, host='127.0.0.1', port=5555):

        self.riemann = Riemann(host, port)
        self.host = myhost
        self.timeprecision = timeprecision

    def shutdown(self):

        return maybeDeferred(self.riemann.shutdown)

    def record(self, service, *args, **kwargs):

        def return_final(nouse, result):

            return result

        def wrap_finished(result, fn, starttime):

            finished_time = round((time.time() - starttime) * 1000, self.timeprecision)
            status = 'ok'

            if float(kwargs.get('ee_criticalthreshold', 0)) > 0:
                if finished_time > float(kwargs.get('ee_criticalthreshold', 0)):
                    status = 'critical'

            return maybeDeferred(self.riemann.submit, {
                'host': self.host,
                'service': str(service),
                'state': status,
                'description': fn.__name__ + "() took " + str(finished_time) + "ms",
                'metric_f': finished_time,
                'tags': fn.__name__
                }).addCallback(return_final, result)

        def decorator(fn):

            @wraps(fn)
            def wrapper(*args, **kwargs):

                starttime = time.time()

                d = maybeDeferred(fn, *args, **kwargs)

                return d.addCallback(wrap_finished, fn, starttime)

            return wrapper

        return decorator

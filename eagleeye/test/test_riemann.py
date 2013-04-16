# -*- test-case-name: eagleeye.test.riemann -*-

from twisted.trial import unittest
from eagleeye.riemann import Riemann
import sys
import base64
import time


class EagleEyeRiemann(unittest.TestCase):

    def setUp(self):

        self.riemann = Riemann('127.0.0.1', 5555)

    def test_sendRiemannSingleMetric(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_f': '13.37', 'time': int(time.time()), 'ttl': 60})

    def test_sendRiemannMultipleMetrics(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part1', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_f': '13.37', 'time': int(time.time()), 'ttl': 60})

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part2', 'state': 'warning', 'description': 'EagleEye.Riemann is working!', 'metric_f': '7'})

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part3', 'state': 'critical', 'description': 'EagleEye.Riemann is working!', 'metric_f': '0'})

    def test_sendRiemannSingleMetricSINT64(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_sint64': sys.maxint })

    def test_format_message_float(self):

        generated = base64.b64encode(self.riemann._format_message({'host':'EagleEye', 'service': 'EagleEye_API', 'state': 'critical', 'description': 'EagleEye.Riemann is working!', 'metric_f': '0', 'time': 1366127369, 'ttl': 100}))
        knowngood = "MlAIiea1iwUSCGNyaXRpY2FsGgxFYWdsZUV5ZV9BUEkiCEVhZ2xlRXllKhxFYWdsZUV5ZS5SaWVtYW5uIGlzIHdvcmtpbmchRQAAyEJ9AAAAAA=="

        self.assertEqual(generated, knowngood)

    def test_format_message_SINT64(self):

        generated = base64.b64encode(self.riemann._format_message({'host':'EagleEye', 'service': 'EagleEye_API', 'state': 'critical', 'description': 'EagleEye.Riemann is working!', 'metric_sint64': 223372036854775999, 'time': 1366127369, 'ttl': 100}))
        knowngood = "MlUIiea1iwUSCGNyaXRpY2FsGgxFYWdsZUV5ZV9BUEkiCEVhZ2xlRXllKhxFYWdsZUV5ZS5SaWVtYW5uIGlzIHdvcmtpbmchRQAAyEJo/oLg1+PryZkG"

        self.assertEqual(generated, knowngood)

    def tearDown(self):

        self.riemann.shutdown()
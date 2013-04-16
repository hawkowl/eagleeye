# -*- test-case-name: eagleeye.test.riemann -*-

from twisted.trial import unittest
from eagleeye.riemann import Riemann
import sys


class EagleEyeRiemann(unittest.TestCase):

    def setUp(self):

        self.riemann = Riemann('127.0.0.1', 5555)

    def test_sendRiemannSingleMetric(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_f': '13.37'})

    def test_sendRiemannMultipleMetrics(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part1', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_f': '13.37'})

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part2', 'state': 'warning', 'description': 'EagleEye.Riemann is working!', 'metric_f': '7'})

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann_Part3', 'state': 'critical', 'description': 'EagleEye.Riemann is working!', 'metric_f': '0'})

    def test_sendRiemannSingleMetricSINT64(self):

        self.riemann.submit({'host':'EagleEye', 'service': 'EagleEye_Riemann', 'state': 'ok', 'description': 'EagleEye.Riemann is working!', 'metric_sint64': sys.maxint })

    def tearDown(self):

        self.riemann.shutdown()
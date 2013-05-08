# -*- test-case-name: eagleeye.test.metric -*-

from twisted.trial import unittest
from twisted.internet.defer import maybeDeferred
import twisted
from eagleeye.metric import Metric
import sys
import base64
import time


class EagleEyeMetric(unittest.TestCase):

    def setUp(self):

        self.ee = Metric(myhost='EagleEye', timeprecision=2, host='127.0.0.1', port=5555)
        twisted.internet.base.DelayedCall.debug = True

    def test_recordRegularFunction(self):

        @self.ee.record('OneSecondTest')
        def OneSecondTest():

            time.sleep(1)

        OneSecondTest()

    def test_recordRegularFunctionWithThreshold(self):

        @self.ee.record('OneSecondTest', ee_criticalthreshold='5')
        def OneSecondTest_Threshold():

            time.sleep(1)

        OneSecondTest_Threshold()

    def test_recordDeferred(self):

        @self.ee.record('DNSLookup')
        def printResult(address):

            return self.assertEqual(address, '127.0.0.1')

        def returnfakeDNS():

            return '127.0.0.1'

        def fakeDNS(address):

            return maybeDeferred(returnfakeDNS)

        d = fakeDNS('127.0.0.1')
        d.addCallback(printResult)

        return d

    def tearDown(self):

        return self.ee.shutdown()
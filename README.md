# EagleEye v0.2.0

EagleEye is a library for recording metrics inside Twisted applications and other related frameworks (eg. Klein). It consists of a decorator-based metric reporting module and a Twisted and Protocol Buffers based Riemann reporting module.

## Current Status

EagleEye is currently so alpha that it hurts.

## Installation

Clone/download it, run `sudo python setup.py install`.

## Usage

### Riemann Reporting

EagleEye.Riemann currently uses UDP for communication. 

The following example submits a report on behalf of the host `WebServer1`, saying that `MyCoolWebApp`'s API took 72ms to respond. In this example, Riemann is hosted on localhost on port 5555 - change this to fit your configuration.

```
from eagleeye.riemann import Riemann

riemann = Riemann('127.0.0.1', 5555)
riemann.submit({'host':'WebServer1',
                'service': 'MyCoolWebApp_APIResponse',
                'state': 'critical',
                'description': 'my_api_function() took 72ms',
                'metric_f': '72'})
```

The following fields can be sent to Riemann:

* `host` - the host you're sending it from
* `service` - the service the metric is for
* `state` - the state that the service is in. Ones that work in Riemann-Dash are `ok` (green), `warning` (yellow) and `critical` (red).
* `description` - the description of the metric, free-form text. Shows up when you hover over the metric in Riemann-Dash, for example.
* `time` - the time of the event, in Unix time.
* `ttl` - the time in seconds that this state is valid for.
* `metric_f` - the metric, in floating point (converted automatically for you by EagleEye).
* `metric_sint64` - the metric, in a long (converted automatically for you by EagleEye).
* `metric_d` - *does not work in EagleEye yet - please use metric_f*

### Metric Recording

EagleEye.Metric is a little class that does the Riemann reporting for you, as invisibly as possible. It will worry about setting up the Riemann connection with what you pass it initially. You can use the Metric and Riemann bits without conflicting, it seems.

This example sets up a Metric object which you can then use to decorate your functions. For this example, the host is `WebServer1`, reporting for the service `DBOperation`, and all metrics are rounded to 2 places after the decimal point. It will also have a `critical` threshold of 5ms. In this example, Riemann is on localhost on port 5555.

```
from eagleeye.metric import Metric

ee = Metric(myhost='WebServer1', timeprecision=2, host='127.0.0.1', port=5555)

@ee.record('DBOperation', ee_criticalthreshold='5')
def db_operation(stuff, things):

    # code goes here
```

EagleEye.Metric is 'invisible' - it won't block a chain of decorators, even. It also handles Deferreds.

#### Klein Reporting

EagleEye.Metric can also report times for your Klein-using app.

```
@route('/login/process', methods=['POST'])
@ee.record('app_login', ee_criticalthreshold='5')
def pg_login_process(request):

    if request.args.get('username')[0] == "myuser":
        return "hi, myuser!"
    else:
        return "get out of here!"
```

## Developing

Think something could be done better? Let me know by email (hawkowl@outlook.com) or twitter (@hawkieowl) - if you think you can do it better, Patches Accepted(TM)! :)

### EagleEye.riemann

EagleEye uses Twisted for the Riemann UDP communication, and ProtoBuf for sending the metrics data over the wire. The protobuf.py shouldn't have to be changed - if it does, get the latest `.proto` from the Riemann site and compile it with `mkdir pb && protoc --python_out pb proto.proto`.

### EagleEye.metric

EagleEye's reporting code is in eagleeye/metric.py and consists of a class with fun decorator stuff inside it. (It maybe relies on magic.)

### Tests

EagleEye uses Twisted's wonderful Trial framework for running unit tests. To run them, cd to the top level project and run `tools/trial eagleeye`. Tests are in `eagleeye/test/`. Please note that the tests only test sending metrics - you should be looking at Riemann to make sure they show up on the other end, and edit the tests to point to your installation!
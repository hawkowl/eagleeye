# EagleEye v0.1.0

EagleEye is a library for recording metrics inside Twisted applications and other related frameworks (eg. Klein). It consists of a decorator-based generic metric reporting module (in 0.2.0, hopefully) and a Twisted and Protocol Buffers based Riemann reporting module.

## Current Status

EagleEye is currently so alpha that it hurts.

## Installation

No method as of yet, just drop eagleeye/ in the same folder as your project for now.

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

## Developing

Think something could be done better? Let me know by email (hawkowl@outlook.com) or twitter (@hawkieowl) - if you think you can do it better, Patches Accepted(TM)! :)

### EagleEye.riemann

EagleEye uses Twisted for the Riemann UDP communication, and ProtoBuf for sending the metrics data over the wire. The protobuf.py shouldn't have to be changed - if it does, get the latest `.proto` from the Riemann site and compile it with `mkdir pb && protoc --python_out pb proto.proto`.

### EagleEye.metric

Currently not yet in EagleEye - hold on!

### Tests

EagleEye uses Twisted's wonderful Trial framework for running unit tests. To run them, cd to the top level project and run `tools/trial eagleeye`. Tests are in `eagleeye/test/`. Please note that the tests only test sending metrics - you should be looking at Riemann to make sure they show up on the other end, and edit the tests to point to your installation!
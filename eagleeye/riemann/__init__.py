import protobuf as pb

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class RiemannProtocol(DatagramProtocol):

    def send(self, msg, host, port):

        self.transport.write(msg, (host, port))


class Riemann:

    validfields = ['description', 'host', 'service', 'state', 'time', 'ttl']

    def __init__(self, host='127.0.0.1', port=5555):

        self.host = host
        self.port = port

        self.protocol = RiemannProtocol()
        self.udpport = reactor.listenUDP(0, self.protocol)

    def shutdown(self):

        return self.udpport.stopListening()

    def submit(self, edict):

        self.protocol.send(self._format_message(edict), self.host, self.port)

    def _format_message(self, edict):

        ev = pb.Event()

        for k in self.validfields:
            if edict.has_key(k):
                setattr(ev, k, edict[k])

        if 'tags' in edict:
            ev.tags.extend(edict['tags'])

        if 'metric_f' in edict:
            ev.metric_f = float(edict['metric_f'])

        if 'metric_sint64' in edict:
            ev.metric_sint64 = long(edict['metric_sint64'])

        msg = pb.Msg()
        msg.events.extend([ev])

        return msg.SerializeToString()
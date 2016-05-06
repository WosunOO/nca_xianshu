import pecan

from nca47.api.controllers.v1 import firewall
from nca47.api.controllers.v1 import dns
from nca47.api.controllers.v1 import agent


class V1Controller(object):
    def __init__(self):
        return

    @pecan.expose('json')
    def index(self):
        return {"key": "value"}

    @pecan.expose()
    def _lookup(self, kind, *remainder):
        if kind == 'dns':
            return dns.DNSController(), remainder
        elif kind == "firewall":
            return firewall.FirewallController(), remainder
        elif kind == "agent":
            return agent.AgentController(), remainder
        else:
            pecan.abort(404)

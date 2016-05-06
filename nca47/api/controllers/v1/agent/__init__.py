import pecan

from nca47.api.controllers.v1.agent import agent


class AgentController(object):
    def __init__(self):
        return

    @pecan.expose('json')
    def index(self):
        return {"Information": "The url is for DNS base RestApi "
                "interface"}

    @pecan.expose()
    def _lookup(self, kind, *remainder):
        if kind == 'agent':
            return agent.GetAgentController(), remainder
        else:
            pecan.abort(404)

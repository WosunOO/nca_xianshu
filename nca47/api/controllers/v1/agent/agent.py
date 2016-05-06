from nca47.common.i18n import _
from oslo_log import log as logging
from oslo_messaging import RemoteError
from nca47.api.controllers.v1 import base
from pecan import expose
from nca47.manager.central import CentralManager
from nca47.api.controllers.v1 import tools
from nca47.common.exception import Nca47Exception
from nca47.common.exception import BadRequest
from nca47.common.i18n import _LE


LOG = logging.getLogger(__name__)


class GetAgentController(base.BaseRestController):
    def __init__(self):
        self.manager = CentralManager.get_instance()
        super(GetAgentController, self).__init__()

    @expose('json')
    def show(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) > 1:
                raise BadRequest(resource="agent_info get", msg=url)
            context = req.context
            agent_id = args[0]
        # input the snat values with dic format
            response = self.manager.get_agent(context, agent_id)
            return response
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.response.status = 500
            message = exception.value
            return tools.ret_info(self.response.status, message)
        except Exception as e:
            LOG.exception(e)
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

    @expose('json')
    def list(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) > 1:
                raise BadRequest(resource="agent_info getall", msg=url)
            context = req.context
            response = self.manager.get_agents(context)
            return response
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.response.status = 500
            message = exception.value
            return tools.ret_info(self.response.status, message)
        except Exception as e:
            LOG.exception(e)
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

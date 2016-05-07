from nca47.api.controllers.v1 import base
from oslo_serialization import jsonutils as json
from nca47.api.controllers.v1 import base
from nca47.common.i18n import _
from nca47.common.i18n import _LI, _LE
from nca47.common.exception import Nca47Exception
from nca47.common.exception import ParamValueError
from oslo_log import log
from nca47.api.controllers.v1 import tools
from nca47.manager.central import CentralManager
from nca47.common.exception import BadRequest
from oslo_messaging import RemoteError

LOG = log.getLogger(__name__)


class Glsb_zoneController(base.BaseRestController):
    def __init__(self):
        self.manager = CentralManager.get_instance()
        super(Glsb_zoneController, self).__init__()

    def create(self, req, *args, **kwargs):
        try:
            url = req.url
            flag = True
            if len(args) > 1:
                raise BadRequest(resource="gslb_zone create", msg=url)
            context = req.context
            body_values = json.loads(req.body)
            valid_attributes = ['tenant_id', 'name', 'devices', 'syn_server']
#             valid_devices = ["group_name", "device_name"]
            values = tools.validat_values(body_values, valid_attributes)
            obj_devices = body_values["devices"]
#             for key in obj_devices:
#                 tools.validat_values(key, valid_devices)
#             tools.validat_values(body_values["syn_server"], valid_devices)
            for key in obj_devices:
                if body_values["syn_server"] in key:
                    flag = False
            if flag:
                raise ParamValueError(param_name=body_values["syn_server"])
            # input the gslb_zone values with dic format
            LOG.info(_LI("input the gslb_zone values with dic format\
                         is %(json)s"),
                     {"json": body_values})

            response = self.manager.create_gslb_zone(context, values)
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

    def remove(self, req, id, *args, **kwargs):
        try:
            url = req.url
            # if len(args) > 1:
            #     raise BadRequest(resource="gslb_zone del", msg=url)
            context = req.context
            body_values={}
#             body_values = json.loads(req.body)
            gslb_zone_id = id
            body_values["id"] = gslb_zone_id
            # input the gslb_zone values with dic format
            LOG.info(_LI("delete the gslb_zone values with dic format\
                         is %(json)s"),
                     {"json": body_values})

            response = self.manager.del_gslb_zone(context, body_values)
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

    def update(self, req, id, *args, **kwargs):
        try:
            url = req.url
            # if len(args) > 1:
            #     raise BadRequest(resource="gslb_zone del", msg=url)
            context = req.context
            body_values = json.loads(req.body)
            gslb_zone_id = args[0]
            valid_attributes = ['enable', 'devices', 'syn_server']
#             valid_devices = ["group_name", "device_name"]
            values = tools.validat_values(body_values, valid_attributes)
            obj_devices = body_values["devices"]
#             for key in obj_devices:
#                 tools.validat_values(key, valid_devices)
#             tools.validat_values(body_values["syn_server"], valid_devices)
            for key in obj_devices:
                if body_values["syn_server"] in key:
                    flag = False
            if flag:
                raise ParamValueError(param_name=body_values["syn_server"])
            # input the gslb_zone values with dic format
            LOG.info(_LI("update the gslb_zone values with dic format\
                         is %(json)s"),
                     {"json": body_values})

            response = self.manager.update_gslb_zone(
                context, gslb_zone_id, values)
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

    def list(self, req, *args, **kwargs):
        try:
            url = req.url
            # if len(args) > 1:
            #     raise BadRequest(resource="gslb_zone getAll", msg=url)
            context = req.context
            search_opts = {}
            # input the staticnat values with dic format
            LOG.info(_LI("get_all the gslb_zone"))
            response = self.manager.get_gslb_zones(context, search_opts)
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

    def show(self, req, id, *args, **kwargs):
        try:
            url = req.url
            # if len(args) > 1:
            #     raise BadRequest(resource="gslb_zone get", msg=url)
            context = req.context
            body_values = {}
            gslb_zone_id = id
            body_values["id"] = gslb_zone_id
            # input the gslb_zone values with dic format
            LOG.info(_LI("get the staticnat values with dic format\
                         is %(json)s"),
                     {"json": body_values})

            response = self.manager.get_gslb_zone(context, body_values)
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

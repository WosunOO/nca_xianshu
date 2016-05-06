from nca47.manager.central import CentralManager
from nca47.common.exception import BadRequest
from nca47.common.exception import ParamFormatError
from nca47.common.exception import ParamNull
from nca47.common.exception import Nca47Exception
from oslo_log import log
from nca47.common.i18n import _LI, _LE
from oslo_serialization import jsonutils as json
from nca47.api.controllers.v1 import tools
from oslo_messaging import RemoteError
from nca47.api.controllers.v1 import base

LOG = log.getLogger(__name__)


class VLANController(base.BaseRestController):

    """the method vlan operation"""

    def __init__(self):
        self.manager = CentralManager.get_instance()
        super(VLANController, self).__init__()

    def create(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="vlan operation", msg=url)
            json_body = req.body
            context = req.context
            dic = json.loads(json_body)
            LOG.info(_LI("add_vlan body is %(json)s,args is %(args)s,"
                         "kwargs is %(kwargs)s"),
                     {"json": dic, "args": args, "kwargs": kwargs})
            list_ = ['tenant_id', 'dc_name', 'vlan_id',
                     'network_zone', 'ipaddr', "ifnames"]
            dic_body = self.firewall_params(dic, list_)
            response = self.manager.create_vlan(context, dic_body)
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Nca47Exception! error info: ' + e.message))
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            return tools.ret_info(self.response.status, e.value)
        except Exception as e:
            LOG.error(_LE('Exception! error info: ' + e.message))
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

    def remove(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="vlan operation", msg=url)
            json_body = req.body
            context = req.context
            dic = json.loads(json_body)
            LOG.info(_LI("del_vlan body is %(json)s, args is %(args)s,"
                         "kwargs is %(kwargs)s"),
                     {"json": dic, "args": args, "kwargs": kwargs})
            list_ = ['tenant_id', 'dc_name', 'id', 'network_zone', "ifnames"]
            dic_body = self.firewall_params(dic, list_)
            response = self.manager.del_vlan(context, dic_body)
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Nca47Exception! error info: ' + e.message))
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            return tools.ret_info(self.response.status, e.value)
        except Exception as e:
            LOG.error(_LE('Exception! error info: ' + e.message))
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

    def show(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="vlan operation", msg=url)
            json_body = req.body
            context = req.context
            dic = json.loads(json_body)
            LOG.info(_LI("get_vlan body is %(json)s, args is %(args)s,"
                         "kwargs is %(kwargs)s"),
                     {"json": dic, "args": args, "kwargs": kwargs})
            list_ = ['id']
            dic_body = self.firewall_params(dic, list_)
            response = self.manager.get_vlan(context, dic_body)
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Nca47Exception! error info: ' + e.message))
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            return tools.ret_info(self.response.status, e.value)
        except Exception as e:
            LOG.error(_LE('Exception! error info: ' + e.message))
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

    def list(self, req, *args, **kwargs):
        try:
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="vlan operation", msg=url)
            context = req.context
            json_body = req.body
            dic = json.loads(json_body)
            LOG.info(_LI("get_all_vlan body is %(json)s, args is %(args)s,"
                         "kwargs is %(kwargs)s"),
                     {"json": dic, "args": args, "kwargs": kwargs})
            list_ = ['tenant_id', 'dc_name', 'network_zone']
            dic_body = self.firewall_params(dic, list_)
            response = self.manager.get_vlans(context, dic_body)
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Nca47Exception! error info: ' + e.message))
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            return tools.ret_info(self.response.status, e.value)
        except Exception as e:
            LOG.error(_LE('Exception! error info: ' + e.message))
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)

    def firewall_params(self, dic, list_):
        dic = tools.filter_string_not_null(dic, list_)
        dic_key = dic.keys()
        for key in dic_key:
            val_key = dic[key]
            if key == "ifnames":
                flag = tools.is_or_not_list(val_key)
                if flag == "0":
                    raise ParamFormatError(param_name=key)
                elif flag == "1":
                    raise ParamNull(param_name=key)
            elif key == "ipaddr":
                flag = tools.is_or_not_list(val_key)
                if flag == "0":
                    raise ParamFormatError(param_name=key)
                elif flag == "1":
                    raise ParamNull(param_name=key)
                else:
                    for v in dic['ipaddr']:
                        v0 = v.split("/")[0]
                        if not tools._is_valid_ipv4_addr(v0):
                            raise ParamFormatError(param_name=key)
                        v1 = v.split("/")[1]
                        try:
                            v1 = int(v1)
                            if v1 < 0 or v1 > 32:
                                raise ParamFormatError(param_name=key)
                        except Exception:
                            raise ParamFormatError(param_name=key)
            else:
                continue
        return dic

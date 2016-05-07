from nca47.api.controllers.v1 import base
from nca47.common.i18n import _
from nca47.api.controllers.v1 import tools as tool
from oslo_log import log as logging
from nca47.manager import central
from nca47.common.exception import Nca47Exception
from nca47.common.exception import BadRequest
from nca47.common.exception import ParamValueError
from oslo_serialization import jsonutils as json
from nca47.common.i18n import _LE
from oslo_messaging import RemoteError

LOG = logging.getLogger(__name__)


class DnsGmemberController(base.BaseRestController):

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(DnsGmemberController, self).__init__()

    def create(self, req, *args, **kwargs):
        """create the dns gmember"""
        try:
            LOG.info(_("create gmember:body is %(json)s, args is %(args)s,"
                       "kwargs is %(kwargs)s"),
                     {"json": req.body, "args": args, "kwargs": kwargs})
            url = req.url
            if len(args) != 0:
                raise BadRequest(resource="gmember create", msg=url)
            array = ["gslb_zone_name", "tenant_id", "name",
                    "ip", "port", "enable"]
            # get the body
            dic = json.loads(req.body)
            dic_body = self.validat_parms(dic, array)
            context = req.context
            response = self.manager.create_gmember(context, dic_body)
            LOG.info(_("Return of Created Gmember Json is %(response)s !"),
            {"response": response})
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = e.code
            return tool.ret_info(e.code, e.message)
        except RemoteError as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.value)
        except Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.message)

    def update(self, req, *args, **kwargs):
        """update the dns gmember"""
        try:
            LOG.info(_("update gmember:body is %(json)s, args is %(args)s,"
                       "kwargs is %(kwargs)s"),
                     {"json": req.body, "args": args, "kwargs": kwargs})
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="gmember update", msg=url)
            # get the body
            dic = json.loads(req.body)
            list_ = ["enable"]
            dic_body = self.validat_parms(dic, list_)
            c = req.context
            response = self.manager.update_gmember(c, dic_body, args[0])
            LOG.info(_("Return of update gmember JSON  is %(response)s !"),
                     {"response": response})
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = e.code
            return tool.ret_info(e.code, e.message)
        except RemoteError as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            message = e.value
            return tool.ret_info(self.response.status, message)
        except Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.message)

    def remove(self, req, id, *args, **kwargs):
        """delete the dns gmember"""
        try:
            LOG.info(_("delete gmember:body is %(json)s, args is %(args)s, "
                       "kwargs is %(kwargs)s"),
                     {"json": req.body, "args": args, "kwargs": kwargs})
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="gmember remove", msg=url)
            c = req.context
            """from rpc server delete the gmember"""
            response = self.manager.delete_gmember(c, id)
            LOG.info(_("Return of remove gmember JSON  is %(response)s !"),
                     {"response": response})
            return response
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            return tool.ret_info(e.code, e.message)
        except RemoteError as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            message = e.value
            return tool.ret_info(self.response.status, message)
        except Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.message)

    def show(self, req, id, *args, **kwargs):
        """get one of the dns gmember"""
        try:
            LOG.info(_("get a gmember: args is %(args)s, "
                       "kwargs is %(kwargs)s"),
                     {"args": args, "kwargs": kwargs})
            url = req.url
            # if len(args) != 1:
            #     raise BadRequest(resource="gmember query one ", msg=url)
            context = req.context
            response = self.manager.get_one_gmember_db(context, id)
            LOG.info(_("Return of gmember JSON  is %(response)s !"),
                     {"response": response})
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = e.code
            return tool.ret_info(e.code, e.message)
        except RemoteError as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            message = e.value
            return tool.ret_info(self.response.status, message)
        except Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.message)

    def list(self, req, *args, **kwargs):
        """get  all of the dns gmember"""
        try:
            LOG.info(_("Get all gmembers: args is %(args)s, "
                       "kwargs is %(kwargs)s"),
                     {"args": args, "kwargs": kwargs})
            url = req.url
            # if len(args) != 0:
            #     raise BadRequest(resource="gmember query all", msg=url)
            context = req.context
            response = self.manager.get_gmembers_db(context)
            LOG.info(_("Return of get all gmember JSON  is %(response)s !"),
                     {"response": response})
            return response
        except Nca47Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = e.code
            return tool.ret_info(e.code, e.message)
        except RemoteError as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            message = e.value
            return tool.ret_info(self.response.status, message)
        except Exception as e:
            LOG.error(_LE('Exception Message: %s !' % (e.message)))
            LOG.exception(e)
            self.response.status = 500
            return tool.ret_info(self.response.status, e.message)

    def validat_parms(self, values, valid_keys):
        """check the in value is null and nums"""
        recom_msg = tool.validat_values(values, valid_keys)
        dic_key = recom_msg.keys()
        for key in dic_key:
            val_key = recom_msg[key]
            if key == "ip":
                if not tool._is_valid_ipv4_addr(val_key):
                    raise ParamValueError(param_name=key)
            elif key == "port":
                if not tool._is_valid_port(val_key):
                    raise ParamValueError(param_name=key)
            elif key == "enable":
                validat = ["yes", "no"]
                if val_key not in validat:
                    raise ParamValueError(param_name=key)
            else:
                continue
        return recom_msg

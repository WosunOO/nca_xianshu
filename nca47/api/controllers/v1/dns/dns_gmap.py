from oslo_log import log as logging
from oslo_messaging import RemoteError
from nca47.api.controllers.v1 import base
from nca47.api.controllers.v1 import tools
from nca47.common.exception import ParamFormatError
from nca47.common.exception import ParamNull
from nca47.common.exception import ParamValueError
from nca47.common.exception import Nca47Exception
from nca47.common.exception import BadRequest
from nca47.common.exception import NonExistParam
from nca47.common.exception import NotAllowModify
from nca47.common.exception import IllegalParam
from nca47.common.i18n import _
from nca47.common.i18n import _LE
from nca47.manager import central
import json

LOG = logging.getLogger(__name__)


class DnsGMapController(base.BaseRestController):
    """
    ca47 GMap class ,using for add/put/delete/get/getall the GMap info,
    validate parameters whether is legal,handling DB operations and calling rpc
    client's corresponding method to send messaging to agent endpoint
    """

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(DnsGMapController, self).__init__(self)

    def create(self, req, *args, **kwargs):
        """
        Create GMap method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        try:
            values = json.loads(req.body)
            url = req.url
            valid_attrbutes = [
                'tenant_id',
                'name',
            ]
            self.check_ava(valid_attrbutes, values)
            # recom_msg = self.validat_create(values, valid_attrbutes)
            self.check_ava(valid_attrbutes, values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gmaps = self.manager.create_gmap(context, values)
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE("Error exception ! error info:%" + e.message))
            LOG.exception(e)
            return tools.ret_info(self.response.status, e.message)
        except RemoteError as e:
            self.response.status = 500
            message = e.value[3:]
            return tools.ret_info(self.response.status, message)
        except Exception as e:
            LOG.exception(e)
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)
        return gmaps

    def update(self, req, *args, **kwargs):
        """
        Update GMap method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        try:
            values = json.loads(req.body)
            url = req.url
            valid_attrbutes = [
                'enable',
                'algorithm',
                'last_resort_pool',
                'gpool_list',
            ]
            self.check_update(valid_attrbutes, values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gmaps = self.manager.update_gmap(context, values, args[0])
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE("Error exception ! error info:%" + e.message))
            LOG.exception(e)
            return tools.ret_info(self.response.status, e.message)
        except RemoteError as e:
            self.response.status = 500
            message = e.value
            return tools.ret_info(self.response.status, e.message)
        except Exception as e:
            LOG.exception(e)
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)
        return gmaps

    def remove(self, req, *args, **kwargs):
        """
        delete GMap method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        try:
            url = req.url
            # LOG.info(_("The in value body is %(body)s"),{"body",values})
            LOG.info(_("The id is %(id)s"), {"id": args[0]})
            recom_msg = {}
            syngroup = self.manager.delete_gmap(context, args[0])
        except Nca47Exception as e:
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            self.response.status = e.code
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.response.status = 500
            message = exception.value
            return tools.ret_info(self.response.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroup

    def list(self, req, *args, **kwargs):
        """
        get GMaps method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        values = json.loads(req.body)
        try:
            # if 'device' in args:
            #     LOG.info(_("args is %(args)s,kwargs is %(kwargs)s"), {'args': args, 'kwargs': kwargs})
            #     zones = self.manager.list_syngroup(context)
            # else:
            LOG.info(
                _("args is %(args)s,kwargs is %(kwargs)s"), {
                    'args': args, "kwargs": kwargs})
            self.check_search(values)
            syngroup = self.manager.get_gmaps(context,values)
            LOG.info(_("Retrun of get_all_db_zone JSON is %(zones)s !"),
                     {"syngroup": syngroup})
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.response.status = 500
            message = exception.value
            return tools.ret_info(self.response.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroup

    def show(self, req, *args, **kwargs):
        """
        get GMap method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        try:
            LOG.info(_("args is %(args)s"), {"args": args})
            syngroup = self.manager.get_gmap(context, args[0])
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.response.status = 500
            message = exception.value
            return tools.ret_info(self.response.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroup

    def check_ava(self, lis, dic):
        """
        check must exits and values
        :param lis:  is a list ,contain all must exits keys;
        :param dic:  is a dict, contain the body give us keys;
        :return:   not return
        """
        for i in lis:
            if i not in dic.keys():
                raise NonExistParam(param_name=i)
            if not tools.is_not_nil(dic[i]):
                raise ParamNull(param_name=i)
        list1 = [
            "tenant_id",
            "name",
            "enable",
            "algorithm",
            "last_resort_pool",
            "gpool_list"
        ]
        for key in dic.keys():
            if key not in list1:
                raise IllegalParam(param_name=key)

    def check_update(self, lis, dic):
        if 'tenant_id' in dic.keys():
            raise NotAllowModify(param_name="tenant_id")
        if 'name' in dic.keys():
            raise NotAllowModify(param_name="name")
            # for key in dic.keys():
            #     if key not in lis:
            #         raise NotAllowModify(param_name=key)

    def check_search(self, dic):
        lis = ["tenant_id","name","enable","algorithm","last_resort_pool","gpool_list"]
        for key in dic.keys():
            if key not in lis:
                raise IllegalParam(param_name=key)

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
            # recom_msg = self.validat_create(values, valid_attrbutes)
            self.check_create(valid_attrbutes, values)
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

    def update(self, req, id, *args, **kwargs):
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
            values['id'] = id
            url = req.url
            self.check_update(values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gmaps = self.manager.update_gmap(context, values)
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

    def remove(self, req, id, *args, **kwargs):
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
            values = json.loads(req.body)
            values['id'] = id
            self.check_remove(values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gmap = self.manager.delete_gmap(context, values)
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
        return gmap

    def list(self, req, *args, **kwargs):
        """
        get GMaps method
        :param req:
        :param args:
        :param kwargs:
        :return:  return http response
        """
        context = req.context
        search_opts = {}
        search_opts.update(req.GET)
        LOG.info(_("search_opts is %s"), search_opts)
        # values = json.loads(req.body)
        try:
            LOG.info(
                _("args is %(args)s,kwargs is %(kwargs)s"), {
                    'args': args, "kwargs": kwargs})
            self.check_search(search_opts)
            gmap = self.manager.get_gmaps(context, search_opts)
            gmap = self.get_return_convert(gmap)
            LOG.info(_("Retrun of get_all_db_zone JSON is %(gmap)s !"),
                     {"gmap": gmap})
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
        return gmap

    def show(self, req, id, *args, **kwargs):
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
            gmap = self.manager.get_gmap(context, id)
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
        return gmap

    def check_remove(self, dic):
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')

    def check_create(self, lis, dic):
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
        validate_list = [
            "tenant_id",
            "name",
            "enable",
            "algorithm",
            "last_resort_pool",
            "gpool_list"
        ]
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)

    def check_update(self, dic):
        if 'tenant_id' not in dic.keys():
            raise ParamNull(param_name="tenant_id")
        if 'name' in dic.keys():
            raise NotAllowModify(param_name="name")
        validate_list = [
            "tenant_id",
            'id',
            'enable',
            'algorithm',
            'last_resort_pool',
            'gpool_list',
        ]
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')
            # for key in dic.keys():
            #     if key not in lis:
            #         raise NotAllowModify(param_name=key)

    def check_search(self, dic):
        validate_list = [
            "id",
            "tenant_id",
            "name",
            "enable",
            "algorithm",
            "last_resort_pool",
            "gpool_list"]
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)

    def get_return_convert(self, gmap):
        for dic in gmap:
            if 'gpool_list' in dic:
                if dic['gpool_list'] == "":
                    dic['gpool_list'] = []
                else:
                    try:
                        dic['gpool_list'] = eval(dic['gpool_list'])
                    except:
                        pass
        return gmap

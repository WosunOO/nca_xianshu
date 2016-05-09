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
from nca47.common.exception import IllegalParam
from nca47.common.exception import NotAllowModify
from nca47.common.i18n import _
from nca47.common.i18n import _LE
from nca47.manager import central
import json

LOG = logging.getLogger(__name__)


class DnsGPoolController(base.BaseRestController):
    """
    ca47 GPool class ,using for add/put/delete/get/getall the GPool info,
    validate parameters whether is legal,handling DB operations and calling rpc
    client's corresponding method to send messaging to agent endpoint
    """

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(DnsGPoolController, self).__init__(self)

    def create(self, req, *args, **kwargs):
        """
        create GPool method
        :param req:
        :param args:
        :param kwargs:
        :return: return http response
        """
        context = req.context
        try:
            values = json.loads(req.body)
            url = req.url
            # recom_msg = self.validat_create(values, valid_attrbutes)
            self.check_create(values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gpools = self.manager.create_gpool(context, values)
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
        return gpools

    def update(self, req, id, *args, **kwargs):
        """
        update GPool method
        :param req:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            values = json.loads(req.body)
            values['id'] = id
            url = req.url
            self.check_update(values)
            # recom_msg = self.validat_update(values, valid_attrbutes)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gpools = self.manager.update_gpool(context, values)
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
        return gpools

    def remove(self, req, id, *args, **kwargs):
        """
        delete GPool method
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return: return http response
        """
        context = req.context
        try:
            url = req.url
            values = {}
            values.update(kwargs)
            values['id'] = id
            self.check_update(values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            recom_msg = {}
            gmap = self.manager.delete_gpool(context, values)
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
        get GPools method
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return: return http response
        """

        context = req.context
        try:
            search_opts = {}
            search_opts.update(req.GET)
            #values = json.loads(req.body)
            self.check_search(search_opts)
            LOG.info(
                _("args is %(args)s,kwargs is %(kwargs)s"), {
                    'args': args, "kwargs": kwargs})
            gpools = self.manager.get_gpools(context, search_opts)
            gpools = self.get_return_convert(gpools)
            LOG.info(_("Retrun of get_all_db_zone JSON is %(gpool)s !"),
                     {"gpool": gpools})
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
        return gpools

    def show(self, req, id, *args, **kwargs):
        """
        get GPool method
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return: return http response
        """
        context = req.context
        try:
            LOG.info(_("args is %(args)s"), {"args": args})
            gmap = self.manager.get_gpool(context, id)
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

    def check_update(self, dic):
        if 'tenant_id' not in dic.keys():
            raise ParamNull(param_name="tenant_id")
        if 'name' in dic.keys():
            raise NotAllowModify(param_name="name")
        if 'gpool_id' in dic.keys():
            raise NotAllowModify(param_name="gpool_id")
        try:
            if 'ttl' in dic.keys():
                int(dic['ttl'])
        except:
            raise ParamValueError(param_name='ttl')
        if 'enable' in dic.keys():
            if dic['enable'] not in ['yes', 'no']:
                raise ParamValueError(param_name='enable')
        validate_list = [
            "tenant_id",
            'id',
            'gmember_list',
            'max_addr_ret',
            'second_algorithm',
            'ttl',
            'fallback_ip',
            'refcnt',
            'hms',
            'warning',
            'enable',
            'cname',
            'pass',
            'first_algorithm']
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')

    def check_create(self, dic):
        """
        check available and must exits
        :param lis:  is a list ,contain all must exits keys;
        :param dic:  is a dict, contain the body give us keys;
        :return:   not return
        """
        validate_list = ['tenant_id', 'name', 'enable', 'ttl']
        for i in validate_list:
            if i not in dic.keys():
                raise NonExistParam(param_name=i)
                # if not tools.is_not_nil(dic[i]):
                #     raise ParamValueError(param_name=i)
        validate_list = [
            "tenant_id",
            "name",
            'gpool_id',
            'gmember_list',
            'max_addr_ret',
            'second_algorithm',
            'ttl',
            'fallback_ip',
            'refcnt',
            'hms',
            'warning',
            'enable',
            'cname',
            'pass',
            'first_algorithm']
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)
        try:
            int(dic['ttl'])
        except:
            raise ParamValueError(param_name='ttl')
        if dic['enable'] not in ['yes', 'no']:
            raise ParamValueError(param_name='enable')

    def check_search(self, dic):
        validate_list = [
            'id',
            "tenant_id",
            "name",
            'gpool_id',
            'gmember_list',
            'max_addr_ret',
            'second_algorithm',
            'ttl',
            'fallback_ip',
            'refcnt',
            'hms',
            'warning',
            'enable',
            'cname',
            'pass',
            'first_algorithm']
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)

    def check_remove(self, dic):
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')

    def get_return_convert(self,gpool):
        for dic in gpool:
            if 'hms' in dic:
                if dic['hms'] == "":
                    dic['hms'] =[]
                else:
                    try:
                        dic['hms']=eval(dic['hms'])
                    except:
                        pass
            if 'gmember_list' in dic:
                if dic['gmember_list'] == "":
                    dic['gmember_list'] =[]
                else:
                    try:
                        dic['gmember_list']=eval(dic['gmember_list'])
                    except:
                        pass
        return gpool
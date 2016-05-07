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
        self.available_list = [
            "tenant_id",
            "name",
            "gpool_id",
            "gmember_list",
            "max_addr_ret",
            "second_algorithm",
            "ttl",
            "fallback_ip",
            "refcnt",
            "hms",
            "warning",
            "enable",
            "cname",
            "pass",
            "first_algorithm"]

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
            valid_attrbutes = [
                "tenant_id",
                "name",
                "enable",
                "ttl",
            ]
            # recom_msg = self.validat_create(values, valid_attrbutes)
            self.check_ava(valid_attrbutes, values)
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

    def update(self, req, *args, **kwargs):
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
            url = req.url
            self.check_update(values)
            # recom_msg = self.validat_update(values, valid_attrbutes)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            gpools = self.manager.update_gpool(context, values, args[0])
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
            # LOG.info(_("The in value body is %(body)s"),{"body",values})
            LOG.info(_("The id is %(id)s"), {"id": id})
            recom_msg = {}
            syngroup = self.manager.delete_gpool(context, id)
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
            syngroup = self.manager.get_gpools(context, search_opts)
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
            syngroup = self.manager.get_gpool(context, id)
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

    def check_update(self, dic):
        if 'tenant_id' in dic.keys():
            raise NotAllowModify(param_name="tenant_id")
        if 'name' in dic.keys():
            raise NotAllowModify(param_name="name")
        try:
            if 'ttl' in dic.keys():
                int(dic['ttl'])
        except:
            raise ParamValueError(param_name='ttl')
        if 'enable' in dic.keys():
            if dic['enable'] not in ['yes', 'no']:
                raise ParamValueError(param_name='enable')
        for key in dic.keys():
            if key not in self.available_list:
                raise IllegalParam(param_name=key)

    def check_ava(self, lis, dic):
        """
        check available and must exits
        :param lis:  is a list ,contain all must exits keys;
        :param dic:  is a dict, contain the body give us keys;
        :return:   not return
        """
        for i in lis:
            if i not in dic.keys():
                raise NonExistParam(param_name=i)
            # if not tools.is_not_nil(dic[i]):
            #     raise ParamValueError(param_name=i)
        for key in dic.keys():
            if key not in self.available_list:
                raise IllegalParam(param_name=key)
        try:
            int(dic['ttl'])
        except:
            raise ParamValueError(param_name='ttl')
        if dic['enable'] not in ['yes', 'no']:
            raise ParamValueError(param_name='enable')

    def check_search(self, dic):
        for key in dic.keys():
            if key not in self.available_list:
                raise IllegalParam(param_name=key)
    # def validat_create(self, values, valid_keys):
    #     recom_msg = tools.validat_values(values, valid_keys)
    #     return self.validat(recom_msg)
    #
    # def validat_update(self, values, valid_keys):
    #     recom_msg = tools.validat_update_values(values, valid_keys)
    #     return self.validat(recom_msg)
    #
    # def validat(self, values):
    #     """
    #     not use
    #     :param values:
    #     :param valid_keys:
    #     :return:
    #     """
    #     recom_msg = values
    #     for key in values.keys():
    #         if key == "tenant_id":
    #             if not tools.is_not_nil(values['tenant_id']):
    #                 raise ParamNull(param_name=key)
    #         elif key == "name":
    #             if not tools.is_not_nil(values['name']):
    #                 raise ParamNull(param_name=key)
    #         elif key == "enable":
    #             if not tools.is_not_nil(values['enable']):
    #                 raise ParamNull(param_name=key)
    #             if values['enable'] not in ['yes', 'no']:
    #                 raise ParamValueError(param_name=key)
    #         elif key == 'ttl':
    #             try:
    #                 ttl = int(values['ttl'])
    #             except Exception as e:
    #                 raise ParamFormatError(param_name=key)
    #             # if ttl > - 0 and ttl <= 3600:
    #             #     raise ParamFormatError(param_name=key)
    #             recom_msg['ttl'] = ttl
    #         elif key == 'max_addr_ret':
    #             try:
    #                 max_addr_ret = int(values['max_addr_ret'])
    #             except Exception as e:
    #                 raise ParamFormatError(param_name=key)
    #         elif key == "type":
    #             if values['type'] not in ['A', 'CNAME']:
    #                 raise ParamValueError(param_name=key)
    #         elif key == "first_algorithm" or key == 'second_algorithm':
    #             if values[key] not in ['sp', 'fi']:
    #                 raise ParamValueError(param_name=key)
    #         elif key == "fallback_ip":
    #             if not tools._is_valid_ipv4_addr(values['fallback_ip']):
    #                 raise ParamValueError(param_name=key)
    #         elif key == 'hms':
    #             if len(values[key]) <= 0:
    #                 raise ParamValueError(param_name=key)
    #         elif key == 'pass':
    #             try:
    #                 pass_ = int(values['pass'])
    #             except Exception as e:
    #                 raise ParamFormatError(param_name=key)
    #             if pass_ > len(values['hms']):
    #                 raise ParamValueError(param_name=key)
    #         elif key == 'gmember_list':
    #             if len(values[key]) <= 0:
    #                 raise ParamValueError(param_name=key)
    #     if 'first_algorithm' in values.keys() and 'second_algorithm' in values.keys():
    #         if values['first_algorithm'] == values["second_algorithm"]:
    #             raise ParamValueError(
    #                 param_name='first_algrith and second_algrithm')
    #
    #     return recom_msg
    #
    # def not_nesscary(self, values):
    #     """
    #     not use
    #     :param values:
    #     :return:
    #     """
    #     recomsg = values
    #     if 'cname' in values.keys() and values['cname'] != '':
    #         recomsg["max_addr_ret"] = ''
    #         recomsg["first_algorithm"] = ''
    #         recomsg['second_algorithm'] = ''
    #         recomsg["fallback_ip"] = ''
    #         recomsg['hms'] = []
    #         recomsg['pass'] = ''
    #         recomsg['gmember_list'] = []
    #     if 'warning' not in values.keys():
    #         recomsg['warning'] = 'yes'
    #     if 'hms' not in values.keys():
    #         recomsg['hms'] = []
    #     if 'gmember_list' not in values.keys():
    #         recomsg['gmember_list'] = []
    #     return recomsg

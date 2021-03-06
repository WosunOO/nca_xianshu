from oslo_log import log as logging
from oslo_messaging import RemoteError
from nca47.api.controllers.v1 import base
from nca47.api.controllers.v1 import tools
from nca47.common.exception import ParamFormatError
from nca47.common.exception import ParamNull
from nca47.common.exception import Nca47Exception
from nca47.common.exception import BadRequest
from nca47.common.exception import ParamValueError
from nca47.common.exception import NonExistParam
from nca47.common.exception import NotAllowModify
from nca47.common.exception import IllegalParam
from nca47.common.i18n import _
from nca47.common.i18n import _LE
from nca47.manager import central
import json

LOG = logging.getLogger(__name__)


class DnsSyngroupController(base.BaseRestController):
    '''

    '''
    """
    ca47 Syngroup class ,using for add/put/delete/get/getall the Syngroup info,
    validate parameters whether is legal,handling DB operations and calling rpc
    client's corresponding method to send messaging to agent endpoint
    """

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(DnsSyngroupController, self).__init__(self)

    def create(self, req, *args, **kwargs):
        """
        Create syngorup method
        :param req:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            values = json.loads(req.body)
            url = req.url
            valid_attributes = [
                "tenant_id",
                "name",
            ]
            self.check_create(valid_attributes, values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            syngroups = self.manager.create_syngroup(context, values)
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE("Error exception ! error info:%" + e.message))
            LOG.exception(e)
            return tools.ret_info(self.response.status, e.message)
        except RemoteError as e:
            self.response.status = 500
            message = e.value
            return tools.ret_info(self.response.status, message)
        except Exception as e:
            LOG.exception(e)
            self.response.status = 500
            return tools.ret_info(self.response.status, e.message)
        return syngroups

    def update(self, req, id, *args, **kwargs):
        """
        update Syngroup method
        :param req:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            url = req.url
            values = json.loads(req.body)
            values['id'] = id
            LOG.info(_("the in value body if %(body)s"), {'body': values})
            self.check_update(values)
            syngroups = self.manager.update_syngroup(
                context, values)
            # args[0] is id
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE("Error exception! error info: %" + e.message))
            LOG.exception(e)
            return tools.ret_info(e.code, e.message)
        except RemoteError as exception:
            self.reponse.status = 500
            message = exception.value
            return tools.ret_info(self.reponse.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroups

    def remove(self, req, id, *args, **kwargs):
        """
        delete the syngroup method
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            values = json.loads(req.body)
            values['id'] = id
            self.check_remove(values)
            LOG.info(_('the in value body is %(body)s'), {'body': values})
            syngroup = self.manager.delete_syngroup(context, values)
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

    def get(self, req, *args, **kwargs):
        """
        # get info for one or more
        :param req:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            LOG.info(
                _("args is %(args)s,kwargs is %(kwargs)s"), {
                    'args': args, "kwargs": kwargs})
            syngroup = self.manager.get_syngroups(context)
            LOG.info(_("Retrun of get_all_db_zone JSON is %(syngroup)s !"),
                     {"syngroup": syngroup})
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            message = e.value
            return tools.ret_info(self.response.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroup

    def list(self, req, *args, **kwargs):
        """
        list all syngroup method
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return:
        """
        context = req.context
        try:
            search_opts = {}
            search_opts.update(req.GET)
            # values = json.loads(req.body)
            # if 'device' in args:
            #     LOG.info(_("args is %(args)s,kwargs is %(kwargs)s"),
            #              {'args': args, 'kwargs': kwargs})
            #     zones = self.manager.list_syngroup(context)
            # else:
            LOG.info(
                _("args is %(args)s,kwargs is %(kwargs)s"), {
                    'args': args, "kwargs": kwargs})
            self.check_search(search_opts)
            syngroup = self.manager.get_syngroups(context, search_opts)
            LOG.info(_("Retrun of get_all_db_zone JSON is %(syngroup)s !"),
                     {"syngroup": syngroup})
        except Nca47Exception as e:
            self.response.status = e.code
            LOG.error(_LE('Error exception! error info: %' + e.message))
            LOG.exception(e)
            return tools.ret_info(e.code, e.message)
        except RemoteError as e:
            self.response.status = 500
            message = e.value
            return tools.ret_info(self.response.status, message)
        except Exception as exception:
            LOG.exception(exception)
            self.response.status = 500
            return tools.ret_info(self.response.status, exception.message)
        return syngroup

    def show(self, req, id, *args, **kwargs):
        """
        get syngroup by id
        :param req:
        :param id:
        :param args:
        :param kwargs:
        :return: return http response
        """
        context = req.context
        try:
            LOG.info(_("args is %(args)s"), {"args": args})
            syngroup = self.manager.get_syngroup(context, id)
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

    def check_search(self, dic):
        validate_list = ['tenant_id', 'name', 'gslb_zone_names', 'pass', 'probe_range']
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)

    def check_update(self, dic):
        if 'tenant_id' not in dic.keys():
            raise ParamNull(param_name="tenant_id")
        if 'name' in dic.keys():
            raise NotAllowModify(param_name="name")
        validate_list = [
                "tenant_id","id","gslb_zone_names", "probe_range", "pass"
            ]
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')
        if 'pass' in dic.keys():
            try:
                int(dic['pass'])
            except:
                ParamValueError(param_name='pass')

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
        validate_list = ['gslb_zone_names', 'pass', 'probe_range',
                 'tenant_id', 'name']
        for key in dic.keys():
            if key not in validate_list:
                raise IllegalParam(param_name=key)
        if 'pass' in dic.keys():
            try:
                int(dic['pass'])
            except:
                ParamValueError(param_name='pass')
        if 'probe_range' in dic.keys():
            if dic['probe_range'] not in [
                    'local_only', 'local_first', 'all_dc', ""]:
                raise ParamValueError(param_name='probe_range')

    def check_remove(self, dic):
        if 'id' not in dic.keys():
            raise ParamNull(param_name='id')

    def get_return_convert(self,syngroup):
        for dic in syngroup:
            if 'gslb_zone_names' in dic:
                if dic['gslb_zone_names'] == "":
                    dic['gslb_zone_names'] =[]
                else:
                    try:
                        dic['gslb_zone_names']=eval(dic['gslb_zone_names'])
                    except:
                        pass
        return syngroup
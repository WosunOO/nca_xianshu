from oslo_log import log as logging
from oslo_messaging import RemoteError
from nca47.api.controllers.v1 import base
from nca47.api.controllers.v1 import tools
from nca47.common.exception import NonExistParam
from nca47.common.exception import ParamFormatError
from nca47.common.exception import ParamNull
from nca47.common.exception import ParamValueError
from nca47.common.exception import Nca47Exception
from nca47.common.exception import BadRequest
from nca47.common.i18n import _
from nca47.common.i18n import _LE
from nca47.manager import central
from oslo_serialization import jsonutils as json
from nca47.api.controllers.v1.tools import check_areaname
from nca47.api.controllers.v1.tools import check_ttl
from nca47.api.controllers.v1.tools import check_renewal
from nca47.api.controllers.v1.tools import is_not_list

LOG = logging.getLogger(__name__)


class DnsZonesController(base.BaseRestController):

    """
    nca47 dnsZones class, using for add/delete/update/query the zones info,
    validate parameters whether is legal, handling DB operations and calling
    rpc client's corresponding method to send messaging to agent endpoints
    """

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(DnsZonesController, self).__init__()

    def create(self, req, *args, **kwargs):
        """create the dns zones"""
        # get the context
        context = req.context
        try:
            # get the body
            values = json.loads(req.body)
            # get the url
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="zone create", msg=url)
            if 'default_ttl' not in values.keys():
                values['default_ttl'] = "3600"
            if 'renewal' not in values.keys():
                raise NonExistParam(param_name='renewal')
            if values['renewal'] == 'no':
                # check the in values
                valid_attributes = ['name', 'owners', 'default_ttl', 'renewal',
                                    'tenant_id']
            elif values['renewal'] == 'yes':
                # check the in values
                valid_attributes = ['name', 'owners', 'default_ttl', 'renewal',
                                    'zone_content', 'slaves', 'tenant_id']
            else:
                raise ParamValueError(param_name='renewal')
            # check the in values
            recom_msg = self.validat_parms(values, valid_attributes)
            LOG.info(_("the in value body is %(body)s"), {"body": values})
            # from rpc server create the zones in db and device
            zones = self.manager.create_zone(context, recom_msg)
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
        return zones

    def update(self, req, id, *args, **kwargs):
        """update the dns zones by currentUser/owners"""
        # get the context
        context = req.context
        try:
            # get the url
            url = req.url
            # if len(args) > 2:
            #     raise BadRequest(resource="zone update", msg=url)
            # get the body
            values = json.loads(req.body)
            LOG.info(_("the in value body is %(body)s"), {"body": values})
            LOG.info(_("the id is %(id)s"), {"id": id})
            if len(args) is 2:
                if args[1] == 'owners':
                    # check the in values
                    valid_attributes = ['id', 'tenant_id', 'owners']
                    recom_msg = self.validat_parms(values, valid_attributes)
                    # from rpc server update the zones in db and device
                    zones = self.manager.update_zone_owners(context, recom_msg,
                                                            recom_msg['id'])
                else:
                    # return the wrong message
                    raise BadRequest(resource="zone update", msg=url)
            else:
                # check the in values
                valid_attributes = ['id', 'tenant_id', 'default_ttl']
                recom_msg = self.validat_parms(values, valid_attributes)
                # from rpc server update the zones in db and device
                zones = self.manager.update_zone(context, recom_msg,
                                                 recom_msg['id'])
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
        return zones

    def remove(self, req, *args, **kwargs):
        """delete the dns zones"""
        # get the context
        context = req.context
        try:
            # get the url
            url = req.url
            if len(args) != 1:
                raise BadRequest(resource="zone delete", msg=url)
            # get the body
            values = json.loads(req.body)
            LOG.info(_("the in value body is %(body)s"), {"body": values})
            # check the in values
            valid_attributes = ['tenant_id', 'id']
            recom_msg = self.validat_parms(values, valid_attributes)
            # from rpc server delete the zones in db and device
            zones = self.manager.delete_zone(context, recom_msg['id'])
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
        return zones

    def list(self, req, *args, **kwargs):
        """get the list of the dns zones"""
        # get the context
        context = req.context
        try:
            if kwargs.get('device'):
                LOG.info(_(" args is %(args)s, kwargs is %(kwargs)s"),
                         {"args": args, "kwargs": kwargs})
                # from rpc server get the zones in device
                zones = self.manager.get_zones(context)
            else:
                LOG.info(_(" args is %(args)s, kwargs is %(kwargs)s"),
                         {"args": args, "kwargs": kwargs})
                # from rpc server get the zones in db
                zones = self.manager.get_all_db_zone(context)
                LOG.info(_("Return of get_all_db_zone JSON is %(zones)s !"),
                         {"zones": zones})
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
        return zones

    def show(self, req, id, *args, **kwargs):
        """get one dns zone info"""
        # get the context
        context = req.context
        try:
            if kwargs.get('device'):
                LOG.info(_(" args is %(args)s"), {"args": args})
                # from rpc server get the zone in device
                zones = self.manager.get_zones(context)
            else:
                LOG.info(_(" args is %(args)s"), {"args": args})
                # from rpc server get the zone in db
                zones = self.manager.get_zone_db_details(context, id)
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
        return zones

    def validat_parms(self, values, valid_keys):
        """check the in value is null and nums"""
        recom_msg = tools.validat_values(values, valid_keys)
        for value in recom_msg:
            if value == "name":
                try:
                    spe_char = '.'
                    char = values[value][-1]
                    if not cmp(spe_char, char):
                        recom_msg[value] = values[value][:-1]
                    if not check_areaname(recom_msg[value]):
                        raise ParamFormatError(param_name=value)
                except Exception:
                    raise ParamFormatError(param_name=value)
            elif value == "default_ttl":
                if not check_ttl(values['default_ttl']):
                    raise ParamFormatError(param_name=value)
            elif value == "renewal":
                if not check_renewal(values['renewal']):
                    raise ParamValueError(param_name=value)
            elif value == "owners":
                flag = is_not_list(values['owners'])
                if flag == "0":
                    raise ParamFormatError(param_name=value)
                elif flag == "1":
                    raise ParamNull(param_name=value)
            elif value == "slaves":
                flag = is_not_list(values['slaves'])
                if flag == "0":
                    raise ParamFormatError(param_name=value)
                elif flag == "1":
                    raise ParamNull(param_name=value)
        return recom_msg

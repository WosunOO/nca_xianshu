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

LOG = logging.getLogger(__name__)


class RegionMemberController(base.BaseRestController):

    """
    nca47 Region Member class, using for add/delete the regions info,
    validate parameters whether is legal, handling DB operations and calling
    rpc client's corresponding method to send messaging to agent endpoints
    """

    def __init__(self):
        self.manager = central.CentralManager.get_instance()
        super(RegionMemberController, self).__init__()

    def create(self, req, *args, **kwargs):
        """create the user region members"""
        # get the context
        context = req.context
        try:
            # get the body
            values = json.loads(req.body)
            # get the url
            url = req.url
            # if len(args) != 1:
            #     raise BadRequest(resource="region member create", msg=url)
            # check the in values
            valid_attributes = ['tenant_id', 'type', 'region_uuid', 'data1']
            # check the in values
            recom_msg = self.validat_parms(values, valid_attributes)
            LOG.info(_("the in value body is %(body)s"), {"body": values})
            # from rpc server create the region members in db and device
            regions = self.manager.create_member(context, recom_msg)
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
        return regions

    def remove(self, req, id, *args, **kwargs):
        """delete the dns region members"""
        # get the context
        context = req.context
        try:
            # get the body
            values = {}
            values.update(kwargs)
            values['id'] = id
            # get the url
            url = req.url
            # if len(args) != 1:
            #     raise BadRequest(resource="region member delete", msg=url)
            # check the in values
            valid_attributes = ['tenant_id', 'id']
            # check the in values
            recom_msg = self.validat_parms(values, valid_attributes)
            LOG.info(_("the in value body is %(body)s"), {"body": values})
            # from rpc server delete the region members in db and device
            regions = self.manager.delete_member(context, recom_msg['id'])
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
        return regions

    def list(self, req, *args, **kwargs):
        """get the list of the dns members"""
        # get the context
        context = req.context
        try:
            # get the body
            values = {}
            values.update(kwargs)
            LOG.info(_(" args is %(args)s, kwargs is %(kwargs)s"),
                     {"args": args, "kwargs": kwargs})
            # check the in values
            valid_attributes = ['tenant_id']
            recom_msg = self.validat_parms(values, valid_attributes)
            # from db server get the get_members in db
            members = self.manager.get_db_members(context, recom_msg)
            LOG.info(_("Return get_members JSON is %(members)s !"),
                     {"members": members})
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
        return members

    def validat_parms(self, values, valid_keys):
        """check the in value is null and nums"""
        recom_msg = tools.validat_values(values, valid_keys)
        for value in recom_msg:
            if value == "type":
                type_array = ['ip_subnet', 'region', 'ISP', 'country',
                              'province']
                if values['type'] not in type_array:
                    raise ParamValueError(param_name=value)
        return recom_msg

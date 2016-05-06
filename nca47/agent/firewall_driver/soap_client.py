from nca47.common.i18n import _
from suds.client import Client
from oslo_config import cfg
from nca47.common.exception import DerviceError as derviceError
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

FW_AGENT_OPTS = [
    cfg.StrOpt('fw_username',
               default='username',
               help=_('The username on which nca47-fw_driver listens.')),
    cfg.StrOpt('fw_passwd',
               default='passwd',
               help=_('The passwd on which nca47-fw_driver listens.')),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='fw_agent',
                         title='Options for the nca47-fw_driver service')
CONF.register_group(opt_group)
CONF.register_opts(FW_AGENT_OPTS, opt_group)

SOAP_CLIENT = None
username = None
passwd = None


class fw_client():
    def __init__(self):
        self.username = CONF.fw_agent.fw_username
        self.passwd = CONF.fw_agent.fw_passwd
        return

    @classmethod
    def get_instance(cls):
        global SOAP_CLIENT
        if not SOAP_CLIENT:
            SOAP_CLIENT = cls()
        return SOAP_CLIENT

    def get_client(self, url):
        try:
            client = Client(url, username=self.username, password=self.passwd)
            service = client.service
        except Exception as e:
            raise derviceError
        return service

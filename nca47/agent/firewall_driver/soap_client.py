from nca47.common.i18n import _
from suds.client import Client
from oslo_config import cfg
from nca47.common.exception import DerviceError as derviceError
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

BACKEND_FW_OPTS = [
    cfg.StrOpt('host',
               default='127.0.0.1',
               help=_('The server hostname/ip to connect to.')),
    cfg.StrOpt('username',
               default='username',
               help=_('The username which use for connect backend '
                      'firewall device')),
    cfg.StrOpt('password',
               default='password',
               help=_('The password which use to connect backend '
                      'firewall device')),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='firewall_backend',
                         title="The backend firewall device's access infos")
CONF.register_group(opt_group)
CONF.register_opts(BACKEND_FW_OPTS, opt_group)

SOAP_CLIENT = None
username = None
passwd = None


class fw_client():

    def __init__(self):
        self.host = CONF.firewall_backend.host
        self.username = CONF.firewall_backend.username
        self.passwd = CONF.firewall_backend.passwd

    @classmethod
    def get_instance(cls):
        global SOAP_CLIENT
        if not SOAP_CLIENT:
            SOAP_CLIENT = cls()
        return SOAP_CLIENT

    def get_client(self, url_dir):
        try:
            ip_link = 'http://%s' % self.host
            full_url = "%s%s" % (ip_link, url_dir)
            client = Client(full_url, username=self.username,
                            password=self.passwd)
            service = client.service
        except Exception as e:
            raise derviceError
        return service

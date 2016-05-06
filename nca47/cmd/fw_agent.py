import sys

from oslo_config import cfg
from nca47.common import service as nca47_service
from nca47.manager import service
sys.path.append('/vagrant/nca47')


def main():
    nca47_service.prepare_service(sys.argv)
    launcher = nca47_service.process_launcher()
    server = service.FWService(topic='firewall_manager')
    launcher.launch_service(server)
    launcher.wait()

if __name__ == '__main__':
    sys.exit(main())

from oslo_serialization import jsonutils as json
from oslo_config import cfg
from oslo_log import log as logging
from nca47.agent.firewall_driver import soap_client
from nca47.api.controllers.v1 import tools
from nca47.common.exception import DerviceError as derviceError

CONF = cfg.CONF
LOG = logging.getLogger(__name__)
FW_DRIVER = None


class fw_driver(object):

    def __init__(self):
        self.ws_client = soap_client.fw_client.get_instance()

    @classmethod
    def get_instance(cls):
        global FW_DRIVER
        if not FW_DRIVER:
            FW_DRIVER = cls()
        return FW_DRIVER

    def create_vlan(self, context, view, dic):
        """  creat vlan to webservice  """
        vlanId = dic["vlan_id_o"]
        ipAddr = tools.joinString(dic["ipaddr"])
        ifNames = tools.joinString(dic["ifnames"])
        ws_ip = "http://" + view['agent_nat_ip']
        other_ip = "/func/web_main/wsdl/vlan/vlan.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("creat vlan to webservice: " + url)
        service = self.ws_client.get_client(url)
        vlan_dic = {}
        vlan_dic['vlanId'] = vlanId
        vlan_dic['ipAddr'] = ipAddr
        vlan_dic['ifNames'] = ifNames
        try:
            response = service.addVlan(**vlan_dic)
        except Exception as e:
            raise derviceError
        # TODO zhuxy return , print only for test
        return response

    def del_vlan(self, context, view, dic):
        """  del vlan to webservice  """
        vlanId = dic["vlan_id_o"]
        ifNames = dic["ifnames"]
        ws_ip = view['agent_nat_ip']
        other_ip = "/func/web_main/wsdl/vlan/vlan.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("del vlan to webservice: " + url)
        client = self.ws_client.get_client(url)
        vlan_dic = {}
        vlan_dic['vlanId'] = vlanId
        vlan_dic['ifNames'] = ifNames
        response = client.service.delVlan(vlanId, ifNames)
        # TODO zhuxy return , print only for test
        print json.loads(response)

    def get_dev_vlan(self, context, view, dic):
        """  get a vlan to webservice  """
        vlanId = dic["vlan_id"]
        ws_ip = view['agent_nat_ip']
        other_ip = "/func/web_main/wsdl/vlan/vlan.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get a vlan to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getVlan(vlanId)
        # TODO zhuxy return , print only for test
        print json.loads(response)

    def get_dev_vlans(self, context, view, dic):
        """  get vlans to webservice  """
        ws_ip = view['agent_nat_ip']
        other_ip = "/func/web_main/wsdl/vlan/vlan.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get vlans to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getVlanAll()
        # TODO zhuxy return , print only for test
        print json.loads(response)

    # this is a netservice operation
    def creat_netservice(self, context, view, dic):
        """  creat netservice to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        proto = dic["proto"]
        port = dic["port"]
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netservice/netservice.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("creat netservice to webservice: " + url)
        client = self.ws_client.get_client(url, name, proto, port, vfwName)
        response = client.service.getVlanAll()
        # TODO zhuxy return , print only for test
        print json.loads(response)

    def del_netservice(self, context, view, dic):
        """  delete netservice to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netservice/netservice.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("delete netservice to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.delService(name, vfwName)
        # TODO zhuxy return , print only for test
        print json.loads(response)

    def get_dev_netservice(self, context, view, dic):
        """  get a netservice to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netservice/netservice.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get a netservice to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getService(name, vfwName)
        # TODO zhuxy return , print only for test
        print json.loads(response)

    def get_dev_netservices(self, context, view, dic):
        """  get all netservices to webservice  """
        ws_ip = view['agent_nat_ip']
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netservice/netservice.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get all netservices to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getServiceAll(vfwName)
        # TODO zhuxy return , print only for test
        print json.loads(response)

    # this is a addrobj operation
    def add_addrobj(self, context, view, dic):
        """  create addrobj to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        ip = dic["ip"]
        vfwName = dic["vfwname"]
        expIp = dic["ip"]
        other_ip = "/func/web_main/wsdl/netaddr/netaddr.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("create addrobj to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.addAddrObj(name, ip, expIp, vfwName)
        # TODO return , print only for test
        print json.loads(response)

    def del_addrobj(self, context, view, dic):
        """  delete addrobj to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netaddr/netaddr.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("delete addrobj to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.delAddrObj(name, vfwName)
        # TODO return , print only for test
        print json.loads(response)

    def get_dev_addrobj(self, context, view, dic):
        """  get a addrobj to webservice  """
        ws_ip = view['agent_nat_ip']
        name = dic["name"]
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netaddr/netaddr.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get a addrobj to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getAddrObj(name, vfwName)
        # TODO return , print only for test
        print json.loads(response)

    def get_dev_addrobjs(self, context, view, dic):
        """  get a addrobj to webservice  """
        ws_ip = view['agent_nat_ip']
        vfwName = dic["vfwname"]
        other_ip = "/func/web_main/wsdl/netaddr/netaddr.wsdl"
        url = "%s%s" % (ws_ip, other_ip)
        LOG.info("get a addrobj to webservice: " + url)
        client = self.ws_client.get_client(url)
        response = client.service.getAddrObjAll(vfwName)
        # TODO return , print only for test
        print json.loads(response)

    def create_packetfilter(self, context, packet_info_dict, agent_info_dict):
        """create packetfilter"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/wsdl/pf_policy/pf_policys/pf_policys.wsdl'
        trans_info_dict = {
            'name': '',
            'srcZoneName': '',
            'dstZoneName': "",
            "srcIpObjNames": '',
            'dstIpObjNames': "",
            'serviceNames': '',
            'action': '',
            'log': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in packet_info_dict.keys():
                trans_info_dict[key] = str(packet_info_dict[key.lower()])
        client = self.ws_client.get_client(url)
        LOG.info("create fw_packetfilter:" + url)
        ret = client.addPacketFilter(**packet_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def delete_packetfilter(self, context, packet_info_dict, agent_info_dict):
        """delete packetfilter"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/pf_policy/pf_policy/pf_policy'
        client = self.ws_client.get_client(url)
        LOG.info("delete fw_packetfilter:" + url)
        trans_info_dict = {
            'name': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in packet_info_dict.keys():
                trans_info_dict[key] = str(packet_info_dict[key.lower()])
        client = self.ws_client.get_client(url)
        LOG.info("create fw_packetfilter:" + url)
        ret = client.delPacketFilter(**packet_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def get_dev_packetfilter(self, context, packet_info_dict, agent_info_dict):
        """get packetfilter"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("get fw_SecurityZone:" + url)
        trans_info_dict = {
            'name': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in packet_info_dict.keys():
                trans_info_dict[key] = packet_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getZone(**packet_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def getall_dev_packetfilter(self, context,
                                packet_info_dict, agent_info_dict):
        """GetAll packetfilter"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("getall fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'name': '',
        }
        for key in trans_info_dict.keys():
            if key.lower() in packet_info_dict.keys():
                trans_info_dict[key] = packet_info_dict[key.lower()]
        ret = client.getZoneAll(**packet_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def create_securityzone(self, context, zone_info_dict, agent_info_dict):
        """create securityZone"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("create fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'name': '',
            'ifNames': '',
            'priority': '',
            'vfwName': '',
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = str(zone_info_dict[key.lower()])
        ret = client.addZone(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def delete_securityzone(self, context, zone_info_dict, agent_info_dict):
        """delete SecurityZone"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("delete fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'id': '',
            'tenant_id': '',
            'dc_name': '',
            'network_zone': '',
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = str(zone_info_dict[key.lower()])
        ret = client.delZone(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def get_dev_securityzone(self, context, zone_info_dict, agent_info_dict):
        """get SecurityZone if """
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("get fw_SecurityZone:" + url)
        trans_info_dict = {
            'name': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = zone_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.addZoneIf(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def getall_dev_securityzone(
            self,
            context,
            zone_info_dict,
            agent_info_dict):
        """GetAll SecurityZone"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("getall fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'name': '',
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = zone_info_dict[key.lower()]
        ret = client.getZoneAll(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def securityzone_addif(self, context, zone_info_dict, agent_info_dict):
        """GetAll SecurityZone"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("addif fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'ifName': '',
            'zoneName': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = zone_info_dict[key.lower()]
        ret = client.addZoneIf(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def securityzone_delif(self, context, zone_info_dict, agent_info_dict):
        """GetAll SecurityZone"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/security_zone/security_zone'
        LOG.info("delif fw_SecurityZone:" + url)
        client = self.ws_client.get_client(url)
        trans_info_dict = {
            'ifName': '',
        }
        for key in trans_info_dict.keys():
            if key.lower() in zone_info_dict.keys():
                trans_info_dict[key] = zone_info_dict[key.lower()]
        ret = client.delZoneIf(**zone_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def create_staticnat(self, context, static_info_dict, agent_info_dict):
        """create StaticNat"""
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("create fw_StaticNat:" + url)
        trans_info_dict = {
            'name': '',
            'srcZoneName': '',
            'dstZoneName': '',
            'srcIpObjNames': '',
            'dstIpObjNames': '',
            'serviceNames': '',
            'action': '',
            'log': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in static_info_dict.keys():
                trans_info_dict[key] = str(static_info_dict[key.lower()])
        client = self.ws_client.get_client(url)
        ret = client.addStaticNat(**trans_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def delete_staticnat(self, context, static_info_dict, agent_info_dict):
        # staticnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_StaticNat:" + url)
        trans_info_dict = {
            'name': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in static_info_dict.keys():
                trans_info_dict[key] = static_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.delStaticNat(**trans_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def get_dev_staticnat(self, context, static_info_dict, agent_info_dict):
        # get staticnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_StaticNat:" + url)
        trans_info_dict = {
            'name': '',
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in static_info_dict.keys():
                trans_info_dict[key] = static_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getStaticNat(**static_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def getall_dev_staticnat(self, context, static_info_dict, agent_info_dict):
        # get all staticnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_StaticNat:" + url)
        trans_info_dict = {
            'vfwName': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in static_info_dict.keys():
                trans_info_dict[key] = static_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getStaticNatAll(**static_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def create_dnat(self, context, dnat_info_dict, agent_info_dict):
        # create dnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("create fw_DNat:" + url)
        trans_info_dict = {
            'name': '',
            'inIfName': '',
            'wanIp': "",
            "wanTcpPort": "",
            "wanUdpPort": "",
            "lanIpStart": "",
            "lanIpEnd": "",
            "lanIpPort": "",
            "slot": "",
            "vfwName": ""
        }
        for key in trans_info_dict.keys():
            if key.lower() in dnat_info_dict.keys():
                trans_info_dict[key] = dnat_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.addDnat(**dnat_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def delete_dnat(self, context, dnat_info_dict, agent_info_dict):
        # delete dnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_DNat:" + url)
        trans_info_dict = {
            'name': '',
            "vfwName": ""
        }
        for key in trans_info_dict.keys():
            if key.lower() in dnat_info_dict.keys():
                trans_info_dict[key] = dnat_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.delDnat(**dnat_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def get_dev_dnat(self, context, dnat_info_dict, agent_info_dict):
        # get dnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_DNat:" + url)
        trans_info_dict = {
            'name': '',
            "vfwName": ""
        }
        for key in trans_info_dict.keys():
            if key.lower() in dnat_info_dict.keys():
                trans_info_dict[key] = dnat_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getDnat(**dnat_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def getall_dev_dnat(self, context, dnat_info_dict, agent_info_dict):
        # getall dnat
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/nat/nat'
        LOG.info("delete fw_DNat:" + url)
        trans_info_dict = {
            "vfwName": ""
        }
        for key in trans_info_dict.keys():
            if key.lower() in dnat_info_dict.keys():
                trans_info_dict[key] = dnat_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getDnat_all(**dnat_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def create_vfw(self, context, vfw_info_dict, agent_info_dict):
        # create vfw
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/vfw/vfw'
        LOG.info("create fw_vfw:" + url)
        trans_info_dict = {
            'name': '',
            'type': '',
            'resource': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in vfw_info_dict.keys():
                trans_info_dict[key] = vfw_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        vfw = client.addNewVsys(**vfw_info_dict)
        if vfw == 0:
            return 0
        else:
            return 'soap fault'

    def delete_vfw(self, context, vfw_info_dict, agent_info_dict):
        # delete
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/vfw/vfw'
        LOG.info("delete fw_vfw:" + url)
        trans_info_dict = {
            'name': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in vfw_info_dict.keys():
                trans_info_dict[key] = vfw_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.delVsys(**vfw_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def get_dev_vfw(self, context, vfw_info_dict, agent_info_dict):
        # get vfw
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/vfw/vfw'
        LOG.info("get fw_vfw:" + url)
        trans_info_dict = {
            'name': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in vfw_info_dict.keys():
                trans_info_dict[key] = vfw_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getVsys(**vfw_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

    def getall_dev_vfw(self, context, vfw_info_dict, agent_info_dict):
        # getall vfw
        url = agent_info_dict['agent_ip']
        url += '/func/web_main/webservice/vfw/vfw'
        LOG.info("getall fw_vfw:" + url)
        trans_info_dict = {
            'name': ''
        }
        for key in trans_info_dict.keys():
            if key.lower() in vfw_info_dict.keys():
                trans_info_dict[key] = vfw_info_dict[key.lower()]
        client = self.ws_client.get_client(url)
        ret = client.getVsysAll(**vfw_info_dict)
        if ret == 0:
            return 0
        else:
            return 'soap fault'

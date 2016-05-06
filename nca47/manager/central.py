from oslo_config import cfg
from oslo_log import log as logging
from nca47 import objects
from nca47.manager.dns_manager import DNSManager
from nca47.manager.firewall_manager.fw_manager import FirewallManager
from nca47.common import exception
CONF = cfg.CONF
LOG = logging.getLogger(__name__)

CENTRAL_MANAGER = None


class CentralManager(object):

    """
    nca47 central handler class, using for response api client requests,
    dispatch client request to dns, firewall or loadbalancer manager
    """

    def __init__(self):
        self.dns_manager = DNSManager.get_instance()
        self.fw_manager = FirewallManager.get_instance()

    @classmethod
    def get_instance(cls):
        global CENTRAL_MANAGER
        if not CENTRAL_MANAGER:
            CENTRAL_MANAGER = cls()
        return CENTRAL_MANAGER

    def create_zone(self, context, zone):
        """"create new zone"""
        zone_obj = self.dns_manager.create_zone(context, zone)
        return zone_obj

    def update_zone(self, context, zone, id):
        """update target zone"""
        zone_obj = self.dns_manager.update_zone(context, zone, id)
        return zone_obj

    def update_zone_owners(self, context, zone, id):
        """update target zone's owners"""
        zone_obj = self.dns_manager.update_zone_owners(context, zone, id)
        return zone_obj

    def delete_zone(self, context, id):
        """delete target zone"""
        response = self.dns_manager.delete_zone(context, id)
        return response

    def get_zones(self, context):
        """get zones from device"""
        # handling zones method in RPC
        response = self.dns_manager.get_zones(context)
        return response

    def get_zone_db_details(self, context, id):
        """show target zone details info from db"""
        zone_obj = self.dns_manager.get_zone_db_details(context, id)
        return zone_obj

    def get_all_db_zone(self, context):
        """call DB to get all zones"""
        zone_objs = self.dns_manager.get_all_db_zone(context)
        return zone_objs

    def get_dev_records(self, context, zone_id):
        """ get all records from device"""
        records = self.dns_manager.get_dev_records(context, zone_id)
        return records

    def get_db_records(self, context, zone_id):
        """get all records belong special zone from db"""
        records = self.dns_manager.get_db_records(context, zone_id)
        return records

    def get_record_from_db(self, context, record_id):
        """get target record detail info from db"""
        record = self.dns_manager.get_record_from_db(context, record_id)
        return record

    def create_record(self, context, record):
        """create one record for special zone"""
        record = self.dns_manager.create_record(context, record)
        return record

    def update_record(self, context, record):
        """update target record info"""
        record = self.dns_manager.update_record(context, record)
        return record

    def delete_record(self, context, rrs):
        """delete target record"""
        response = self.dns_manager.delete_record(context, rrs)
        return response

    def del_cache(self, context, domain):
        """clean cache from dns device"""
        response = self.dns_manager.del_cache(context, domain)
        return response

    def create_region(self, context, region):
        """"create new region"""
        zone_obj = self.dns_manager.create_region(context, region)
        return zone_obj

    def delete_region(self, context, id):
        """delete target region"""
        response = self.dns_manager.delete_region(context, id)
        return response

    def create_member(self, context, member):
        """"create new member"""
        zone_obj = self.dns_manager.create_member(context, member)
        return zone_obj

    def delete_member(self, context, id):
        """delete target member"""
        response = self.dns_manager.delete_member(context, id)
        return response

    def get_members(self, context):
        """show target region details info from db"""
        zone_obj = self.dns_manager.get_members(context)
        return zone_obj

    def get_region_db_detail(self, context, id):
        """show target region details info from db"""
        zone_obj = self.dns_manager.get_region_db_detail(context, id)
        return zone_obj

    def get_all_db_region(self, context):
        """call DB to get all regions"""
        zone_objs = self.dns_manager.get_all_db_region(context)
        return zone_objs

    def create_sp_policy(self, context, proximity):
        """"create new proximity"""
        zone_obj = self.dns_manager.create_sp_policy(context, proximity)
        return zone_obj

    def delete_sp_policy(self, context, id):
        """delete target proximity"""
        response = self.dns_manager.delete_sp_policy(context, id)
        return response

    def update_sp_policy(self, context, proximity, id):
        """update target proximity"""
        zone_obj = self.dns_manager.update_sp_policy(context, proximity, id)
        return zone_obj

    def get_sp_policy(self, context, id):
        """get policy from device"""
        # handling policy method in RPC
        response = self.dns_manager.get_sp_policy(context, id)
        return response

    def get_sp_policys(self, context):
        """get policys from device"""
        # handling policys method in RPC
        response = self.dns_manager.get_sp_policys(context)
        return response

    def get_proximity_db_detail(self, context, id):
        """show target proximity details info from db"""
        zone_obj = self.dns_manager.get_proximity_db_detail(context, id)
        return zone_obj

    def get_all_db_proximity(self, context):
        """call DB to get all proximitys"""
        zone_objs = self.dns_manager.get_all_db_proximity(context)
        return zone_objs

    def get_gmembers_db(self, context):
        """get all gmembers"""
        response = self.dns_manager.get_gmembers_db(context)
        return response

    def get_one_gmember_db(self, context, gmember_uuid):
        """get a gmember"""
        response = self.dns_manager.get_one_gmember_db(context, gmember_uuid)
        return response

    def create_gmember(self, context, dic):
        """create a gmember"""
        response = self.dns_manager.create_gmember(context, dic)
        return response

    def update_gmember(self, context, dic, gmember_uuid):
        """update gmember info"""
        response = self.dns_manager.update_gmember(context, dic, gmember_uuid)
        return response

    def delete_gmember(self, context, gmember_uuid):
        """delete target gmember"""
        response = self.dns_manager.delete_gmember(context, gmember_uuid)
        return response

    def get_hm_templates_db(self, context):
        """get all hm_templates"""
        response = self.dns_manager.get_hm_templates_db(context)
        return response

    def get_one_hm_template_db(self, context, template_uuid):
        """get a hm_template"""
        return self.dns_manager.get_one_hm_template_db(context,
                                                       template_uuid)

    def create_hm_template(self, context, dic):
        """create a hm_template"""
        response = self.dns_manager.create_hm_template(context, dic)
        return response

    def update_hm_template(self, context, dic, template_uuid):
        """update hm_template info"""
        response = self.dns_manager.update_hm_template(context,
                                                       dic, template_uuid)
        return response

    def delete_hm_template(self, context, template_uuid):
        """delete target hm_template"""
        response = self.dns_manager.delete_hm_template(context, template_uuid)
        return response

    # this is a vlan operation
    def create_vlan(self, context, dic):
        return self.fw_manager.create_vlan(context, dic)

    def del_vlan(self, context, dic):
        return self.fw_manager.del_vlan(context, dic)

    def get_vlan(self, context, dic):
        return self.fw_manager.get_vlan(context, dic)

    def get_vlans(self, context, dic):
        return self.fw_manager.get_vlans(context, dic)

    # this is a netservice operation
    def creat_netservice(self, context, netsev_infos):
        return self.fw_manager.creat_netservice(context, netsev_infos)

    def del_netservice(self, context, netsev_infos):
        return self.fw_manager.del_netservice(context, netsev_infos)

    def get_netservice(self, context, netsev_infos):
        return self.fw_manager.get_netservice(context, netsev_infos)

    def get_netservices(self, context, netsev_infos):
        return self.fw_manager.get_netservices(context, netsev_infos)

    # this is a addrobj operation
    def add_addrobj(self, context, addrobj_infos):
        return self.fw_manager.add_addrobj(context, addrobj_infos)

    def del_addrobj(self, context, addrobj_infos):
        return self.fw_manager.del_addrobj(context, addrobj_infos)

    def get_addrobj(self, context, addrobj_infos):
        return self.fw_manager.get_addrobj(context, addrobj_infos)

    def get_addrobjs(self, context, addrobj_infos):
        return self.fw_manager.get_addrobjs(context, addrobj_infos)

    # this is a snataddrpool operation
    def add_snataddrpool(self, context, snataddrpool_infos):
        return self.fw_manager.add_snataddrpool(context, snataddrpool_infos)

    def del_snataddrpool(self, context, snataddrpool_infos):
        return self.fw_manager.del_snataddrpool(context, snataddrpool_infos)

    def get_snataddrpool(self, context, snataddrpool_infos):
        return self.fw_manager.get_snataddrpool(context, snataddrpool_infos)

    def get_snataddrpools(self, context, snataddrpool_infos):
        return self.fw_manager.get_snataddrpools(context, snataddrpool_infos)

    def create_vfw(self, context, vfw):
        return self.fw_manager.create_vfw(context, vfw)

    def delete_vfw(self, context, vfw):
        return self.fw_manager.delete_vfw(context, vfw)

    def get_vfw(self, context, vfw):
        return self.fw_manager.get_vfw(context, vfw)

    def get_all_vfws(self, context, vfw):
        return self.fw_manager.get_all_vfws(context, vfw)

    def create_dnat(self, context, dnat):
        return self.fw_manager.create_dnat(context, dnat)

    def delete_dnat(self, context, dnat):
        return self.fw_manager.delete_dnat(context, dnat)

    def get_dnat(self, context, dnat):
        return self.fw_manager.get_dnat(context, dnat)

    def get_all_dnats(self, context, dnat):
        return self.fw_manager.get_all_dnats(context, dnat)

    def create_packetfilter(self, context, packetfilter):
        return self.fw_manager.create_packetfilter(context, packetfilter)

    def delete_packetfilter(self, context, packetfilter):
        return self.fw_manager.delete_packetfilter(context, packetfilter)

    def get_packetfilter(self, context, packetfilter):
        return self.fw_manager.get_packetfilter(context, packetfilter)

    def get_all_packetfilters(self, context, packetfilter):
        return self.fw_manager.get_all_packetfilters(context, packetfilter)

    # this is a vfw operation
    def create_vrf(self, context, fw_object):
        return self.fw_manager.create_vrf(context, fw_object)

    def del_vrf(self, context, fw_object):
        return self.fw_manager.del_vrf(context, fw_object)

    def get_vrf(self, context, fw_object):
        return self.fw_manager.get_vrf(context, fw_object)

    def get_vrfs(self, context, fw_object):
        return self.fw_manager.get_vrfs(context, fw_object)

    # this is a snat operation
    def create_snat(self, context, fw_object):
        return self.fw_manager.create_snat(context, fw_object)

    def del_snat(self, context, fw_object):
        return self.fw_manager.del_snat(context, fw_object)

    def get_snat(self, context, fw_object):
        return self.fw_manager.get_snat(context, fw_object)

    def get_snats(self, context, fw_object):
        return self.fw_manager.get_snats(context, fw_object)

    # this is a securityZone operation
    def create_securityZone(self, context, fw_object):
        return self.fw_manager.create_securityZone(context, fw_object)

    def update_securityZone(self, context, fw_object):
        return self.fw_manager.update_securityZone(context, fw_object)

    def del_securityZone(self, context, fw_object):
        return self.fw_manager.del_securityZone(context, fw_object)

    def get_securityZone(self, context, fw_object):
        return self.fw_manager.get_securityZone(context, fw_object)

    def get_securityZones(self, context, fw_object):
        return self.fw_manager.get_securityZones(context, fw_object)

    # this is a staticnat operation
    def create_staticnat(self, context, fw_object):
        return self.fw_manager.create_staticnat(context, fw_object)

    def del_staticnat(self, context, fw_object):
        return self.fw_manager.del_staticnat(context, fw_object)

    def get_staticnat(self, context, fw_object):
        return self.fw_manager.get_staticnat(context, fw_object)

    def get_staticnats(self, context, fw_object):
        return self.fw_manager.get_staticnats(context, fw_object)

    # this is a gslb_zone operation
    def create_gslb_zone(self, context, dns_object):
        return self.dns_manager.create_gslb_zone(context, dns_object)

    def del_gslb_zone(self, context, dns_object):
        return self.dns_manager.del_gslb_zone(context, dns_object)

    def update_gslb_zone(self, context, zone_id, dns_object):
        return self.dns_manager.update_gslb_zone(context, zone_id, dns_object)

    def get_gslb_zone(self, context, dns_object):
        return self.dns_manager.get_gslb_zone(context, dns_object)

    def get_gslb_zones(self, context, dns_object):
        return self.dns_manager.get_gslb_zones(context, dns_object)

    def create_syngroup(self, context, syngroup_dict):
        return self.dns_manager.create_syngroup(context, syngroup_dict)

    def update_syngroup(self, context, syngroup_dict, id):
        return self.dns_manager.update_syngroup(context, syngroup_dict, id)

    def remove_syngroup(self, context, syngroup_id):
        return self.dns_manager.remove_syngroup(context, syngroup_id)

    def get_syngroups(self, context):
        return self.dns_manager.get_db_syngroups(context)

    def get_syngroup(self, context, syngroup_id):
        return self.dns_manager.get_syngroup(context, syngroup_id)

    def delete_syngroup(self, context, syngroup_id):
        return self.dns_manager.delete_syngroup(context, syngroup_id)

    def create_gpool(self, context, gpool_dict):
        return self.dns_manager.create_gpool(context, gpool_dict)

    def update_gpool(self, context, gpool_dict, id):
        return self.dns_manager.update_gpool(context, gpool_dict, id)

    def get_gpools(self, context):
        return self.dns_manager.get_db_gpools(context)

    def get_gpool(self, context, gpool_id):
        return self.dns_manager.get_gpool(context, gpool_id)

    def delete_gpool(self, context, gpool_id):
        return self.dns_manager.delete_gpool(context, gpool_id)

    def create_gmap(self, context, gmap_dict):
        return self.dns_manager.create_gmap(context, gmap_dict)

    def update_gmap(self, context, gmap_dict, id):
        return self.dns_manager.update_gmap(context, gmap_dict, id)

    def get_gmaps(self, context):
        return self.dns_manager.get_db_gmaps(context)

    def get_gmap(self, context, gmap_id):
        return self.dns_manager.get_gmap(context, gmap_id)

    def delete_gmap(self, context, gmap_id):
        return self.dns_manager.delete_gmap(context, gmap_id)

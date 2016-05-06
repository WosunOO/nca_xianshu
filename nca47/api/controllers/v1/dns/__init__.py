import pecan

from nca47.api.controllers.v1.dns import dns_records, dns_hm_template
from nca47.api.controllers.v1.dns import dns_gmember
from nca47.api.controllers.v1.dns import cache_clean
from nca47.api.controllers.v1.dns import dns_zones
from nca47.api.controllers.v1.dns import dns_servers
from nca47.api.controllers.v1.dns import static_proximity
from nca47.api.controllers.v1.dns import user_region_member
from nca47.api.controllers.v1.dns import user_region
from nca47.api.controllers.v1.dns import dns_gslb_zone
from nca47.api.controllers.v1.dns import dns_syngroup
from nca47.api.controllers.v1.dns import dns_gpool
from nca47.api.controllers.v1.dns import dns_gmap

class DNSController(object):
    def __init__(self):
        return

    @pecan.expose('json')
    def index(self):
        return {"Information": "The url is for DNS base RestApi "
                "interface"}

    @pecan.expose()
    def _lookup(self, kind, *remainder):
        if kind == 'record':
            return dns_records.DnsRecordsController(), remainder
        elif kind == 'zones':
            return dns_zones.DnsZonesController(), remainder
        elif kind == 'cache':
            return cache_clean.CacheCleanController(), remainder
        elif kind == "dns_servers":
            return dns_servers.DnsServersController(), remainder
        elif kind == "proximity":
            return static_proximity.ProximityController(), remainder
        elif kind == "member":
            return user_region_member.RegionMemberController(), remainder
        elif kind == "region":
            return user_region.RegionController(), remainder
        elif kind == "gmember":
            return dns_gmember.DnsGmemberController(), remainder
        elif kind == "hm_template":
            return dns_hm_template.DnsHmTemplateController(), remainder
        elif kind == "gslb_zone":
            return dns_gslb_zone.Glsb_zoneController(), remainder
        elif kind == 'syngroup':
            return dns_syngroup.DnsSyngroupController(),remainder
        elif kind =="gpool":
            return dns_gpool.DnsGPoolController(),remainder
        elif kind =="gmap":
            return dns_gmap.DnsGMapController(),remainder
        else:
            pecan.abort(404)

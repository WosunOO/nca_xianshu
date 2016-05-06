import sqlalchemy as sa
from oslo_db.sqlalchemy import types as db_types

from nca47.db.sqlalchemy.models import base as model_base
from nca47.objects import attributes as attr

HasTenant = model_base.HasTenant
HasId = model_base.HasId
HasStatus = model_base.HasStatus
HasOperationMode = model_base.HasOperationMode


class DnsServer(model_base.BASE, HasId, HasOperationMode):
    """Represents a dns server."""

    name = sa.Column(sa.String(attr.NAME_MAX_LEN))


class Zone(model_base.BASE, HasId, HasOperationMode):
    """Represents a dns zone."""

    __tablename__ = 'dns_zone_info'

    zone_name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    zone_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    vres_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    masters = sa.Column(db_types.JsonEncodedList)
    slaves = sa.Column(db_types.JsonEncodedList)
    renewal = sa.Column(sa.String(attr.NAME_MAX_LEN))
    default_ttl = sa.Column(sa.String(attr.NAME_MAX_LEN))
    owners = sa.Column(db_types.JsonEncodedList)
    ad_controller = sa.Column(sa.String(attr.NAME_MAX_LEN))
    comment = sa.Column(sa.String(attr.NAME_MAX_LEN))


class ZoneRecord(model_base.BASE, HasId, HasOperationMode):
    """Represents a dns zone."""

    __tablename__ = 'dns_rrs_info'
    zone_id = sa.Column(sa.String(attr.UUID_LEN))
    rrs_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    rrs_name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    type = sa.Column(sa.String(attr.NAME_MAX_LEN))
    klass = sa.Column(sa.String(attr.NAME_MAX_LEN))
    ttl = sa.Column(sa.String(attr.NAME_MAX_LEN))
    rdata = sa.Column(sa.String(attr.NAME_MAX_LEN))


class HmTemplateInfo(model_base.BASE, HasId, HasOperationMode):
    """Represents a  HmTemplateInfo."""

    __tablename__ = 'hm_template_info'
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    types = sa.Column(sa.String(attr.NAME_MAX_LEN))
    check_interval = sa.Column(sa.String(attr.FIVE_LEN))
    timeout = sa.Column(sa.String(attr.FIVE_LEN))
    max_retries = sa.Column(sa.String(attr.FIVE_LEN))
    sendstring = sa.Column(sa.String(attr.INPUT_MAX_LEN))
    recvstring = sa.Column(sa.String(attr.INPUT_MAX_LEN))
    hm_template_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    refcnt = sa.Column(sa.String(attr.TEN_LEN))
    username = sa.Column(sa.String(attr.NAME_MAX_LEN))
    password = sa.Column(sa.String(attr.NAME_MAX_LEN))
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))


class GslbZoneInfo(model_base.BASE, HasId, HasOperationMode):
    """Represents a GslbZoneInfo."""

    __tablename__ = 'gslb_zone_info'
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    devices = sa.Column(db_types.JsonEncodedList)
    syn_server = sa.Column(sa.String(attr.INPUT_MAX_LEN))
    gslb_zone_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    enable = sa.Column(sa.String(attr.INPUT_MAX_LEN),
                       default='yes')
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))


class GmemberInfo(model_base.BASE, HasId, HasOperationMode):
    """Represents a GmemberInfo."""

    __tablename__ = 'gmember_info'
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    gslb_zone_name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    ip = sa.Column(sa.String(attr.IP_LEN))
    port = sa.Column(sa.String(attr.FIVE_LEN))
    enable = sa.Column(sa.String(attr.FIVE_LEN),
                       default="yes")
    refcnt = sa.Column(sa.String(attr.TEN_LEN))
    gmember_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))


class Region(model_base.BASE, HasId, HasOperationMode):
    """Represents a region info."""

    __tablename__ = 'region_info'
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    region_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    refcnt = sa.Column(sa.String(attr.NAME_MAX_LEN))
    region_user = sa.Column(sa.String(attr.INPUT_MAX_LEN))


class RegionUser(model_base.BASE, HasId, HasOperationMode):
    """Represents a region user info."""

    __tablename__ = 'region_user_info'
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    region_useruser_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    region_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    type = sa.Column(sa.String(attr.NAME_MAX_LEN))
    data1 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    data2 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    data3 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    data4 = sa.Column(sa.String(attr.NAME_MAX_LEN))


class Proximity(model_base.BASE, HasId, HasOperationMode):
    """Represents a proximity info."""

    __tablename__ = 'sp_policy_info'
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    sp_policy_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_type = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_logic = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_data1 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_data2 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_data3 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    src_data4 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    dst_type = sa.Column(sa.String(attr.NAME_MAX_LEN))
    dst_logic = sa.Column(sa.String(attr.NAME_MAX_LEN))
    dst_data1 = sa.Column(sa.String(attr.NAME_MAX_LEN))
    dst_data2 = sa.Column(sa.String(attr.NAME_MAX_LEN))


class Syngroup(model_base.BASE, HasId, HasOperationMode):
    """
    Represents a dns Syngroup_zone
    """
    __tablename__ = 'syngroup_info'
    syngroup_id = sa.Column(sa.String(attr.UUID_LEN))
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    gslb_zone_names = sa.Column(db_types.JsonEncodedList)
    probe_range = sa.Column(sa.String(attr.NAME_MAX_LEN))
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    pass_ = sa.Column(sa.String(attr.FIVE_LEN))


class GPoolInfo(model_base.BASE, HasId, HasOperationMode):
    __tablename__ = 'gpool_info'
    tenant_id = sa.Column(sa.String(attr.UUID_LEN))
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    enable = sa.Column(sa.String(attr.FIVE_LEN))
    pass_ = sa.Column(sa.String(attr.FIVE_LEN))
    ttl = sa.Column(sa.String(attr.TTL_LEN))
    max_addr_ret = sa.Column(sa.String(attr.NAME_MAX_LEN))
    cname = sa.Column(sa.String(attr.NAME_MAX_LEN))
    first_algorithm = sa.Column(sa.String(attr.FIVE_LEN))
    second_algorithm = sa.Column(sa.String(attr.FIVE_LEN))
    fallback_ip = sa.Column(sa.String(attr.IP_LEN))
    hms = sa.Column(db_types.JsonEncodedList)
    gmember_list = sa.Column(db_types.JsonEncodedList)
    warning = sa.Column(sa.String(attr.TYPE_LEN))
    gpool_id = sa.Column(sa.String(attr.NAME_MAX_LEN))


class GMapInfo(model_base.BASE, HasId, HasOperationMode):
    __tablename__ = 'gmap_info'
    tenant_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    gmap_id = sa.Column(sa.String(attr.NAME_MAX_LEN))
    name = sa.Column(sa.String(attr.NAME_MAX_LEN))
    gpool_list = sa.Column(db_types.JsonEncodedList)
    last_resort_pool = sa.Column(sa.String(attr.NAME_MAX_LEN))
    algorithm = sa.Column(sa.String(attr.NAME_MAX_LEN))
    enable = sa.Column(sa.String(attr.TEN_LEN))

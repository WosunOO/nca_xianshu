from nca47.db import api as db_api
from nca47.db.sqlalchemy.models import Syngroup as SyngroupModel
from nca47.objects import base
from nca47.objects import fields as object_fields


class DnsSyngroup(base.Nca47Object):
    VERSION = '1.0'
    fields = {
        #'id': object_fields.StringField(),
        'tenant_id': object_fields.StringField(),
        'name': object_fields.StringField(),
        'gslb_zone_names': object_fields.ListOfStringsField(),
        'probe_range': object_fields.StringField(),
        'syngroup_id': object_fields.StringField(),
        'pass_': object_fields.StringField()
    }

    def __init__(self, context=None, **kwargs):
        self.db_api = db_api.get_instance()
        super(DnsSyngroup, self).__init__(context=None, **kwargs)

    @staticmethod
    def __from_db_object(dns_syngroup, db_dns_syngroup):
        """
        :param dns_syngroup:
        :param db_dns_syngroup:
        :return:
        """
        for field in dns_syngroup.fields:
            dns_syngroup[field] = db_dns_syngroup
        dns_syngroup.obj_reset_changes()
        return dns_syngroup

    def create(self, context, values):
        syngroup = self.db_api.create(SyngroupModel, values)
        return syngroup

    def update(self, context, id, values):
        syngroup = self.db_api.update_object(SyngroupModel, id, values)
        return syngroup

    def get_object(self, context, **values):
        syngroup = self.db_api.get_object(SyngroupModel, **values)
        return syngroup

    def get_objects(self, context, **values):
        syngroup = self.db_api.get_objects(SyngroupModel, **values)
        return syngroup

    def delete(self, context, id):
        syngroup = self.db_api.delete_object(SyngroupModel, id)
        return syngroup

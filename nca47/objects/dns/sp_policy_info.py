from nca47.db import api as db_api
from nca47.db.sqlalchemy.models import Proximity as ProximityModel
from nca47.objects import base
from nca47.objects import fields as object_fields


class ProximityInfo(base.Nca47Object):
    VERSION = '1.0'

    fields = {
        'tenant_id': object_fields.StringField(),
        'sp_policy_id': object_fields.StringField(),
        'src_type': object_fields.StringField(),
        'src_logic': object_fields.StringField(),
        'src_data1': object_fields.StringField(),
        'src_data2': object_fields.StringField(),
        'src_data3': object_fields.StringField(),
        'src_data4': object_fields.StringField(),
        'dst_type': object_fields.StringField(),
        'dst_logic': object_fields.StringField(),
        'dst_data1': object_fields.StringField(),
        'dst_data2': object_fields.StringField(),
    }

    def __init__(self, context=None, **kwarg):
        self.db_api = db_api.get_instance()
        super(ProximityInfo, self).__init__(context=None, **kwarg)

    @staticmethod
    def _from_db_object(dns_proximity, db_dns_proximity):
        """Converts a database entity to a formal :class:`Proximity` object.

        :param dns_proximity: An object of :class:`Proximity`.
        :param db_dns_proximity: A DB model of a Proximity.
        :return: a :class:`Proximity` object.
        """
        for field in dns_proximity.fields:
            dns_proximity[field] = db_dns_proximity[field]

        dns_proximity.obj_reset_changes()
        return dns_proximity

    def create(self, context, values):
        region = self.db_api.create(ProximityModel, values)
        return region

    def update(self, context, id, values):
        region = self.db_api.update_object(ProximityModel, id, values)
        return region

    def get_object(self, context, **values):
        region = self.db_api.get_object(ProximityModel, **values)
        return region

    def delete(self, context, id):
        region = self.db_api.delete_object(ProximityModel, id)
        return region

    def get_objects(self, context, **values):
        region = self.db_api.get_objects(ProximityModel, **values)
        return region

    def get_all_object(self, context, values):
        region = self.db_api.get_all_object(ProximityModel, values)
        return region

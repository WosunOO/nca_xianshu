from nca47.db import api as db_api
from nca47.db.sqlalchemy.models import RegionUser as RegionUserModel
from nca47.objects import base
from nca47.objects import fields as object_fields


class RegionUserInfo(base.Nca47Object):
    VERSION = '1.0'

    fields = {
        'tenant_id': object_fields.StringField(),
        'name': object_fields.StringField(),
        'region_useruser_id': object_fields.StringField(),
        'region_id': object_fields.StringField(),
        'type': object_fields.StringField(),
        'data1': object_fields.StringField(),
        'data2': object_fields.StringField(),
        'data3': object_fields.StringField(),
        'data4': object_fields.StringField(),
    }

    def __init__(self, context=None, **kwarg):
        self.db_api = db_api.get_instance()
        super(RegionUserInfo, self).__init__(context=None, **kwarg)

    @staticmethod
    def _from_db_object(dns_region_user, db_dns_region_user):
        """Converts a database entity to a formal :class:`RegionUser` object.

        :param dns_region_user: An object of :class:`RegionUser`.
        :param db_dns_region_user: A DB model of a RegionUser.
        :return: a :class:`RegionUser` object.
        """
        for field in dns_region_user.fields:
            dns_region_user[field] = db_dns_region_user[field]

        dns_region_user.obj_reset_changes()
        return dns_region_user

    def create(self, context, values):
        region = self.db_api.create(RegionUserModel, values)
        return region

    def update(self, context, id, values):
        region = self.db_api.update_object(RegionUserModel, id, values)
        return region

    def get_object(self, context, **values):
        region = self.db_api.get_object(RegionUserModel, **values)
        return region

    def delete(self, context, id):
        region = self.db_api.delete_object(RegionUserModel, id)
        return region

    def get_objects(self, context, **values):
        region = self.db_api.get_objects(RegionUserModel, **values)
        return region

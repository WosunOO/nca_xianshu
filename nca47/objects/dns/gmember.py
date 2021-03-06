from nca47.db import api as db_api
from nca47.db.sqlalchemy.models import GmemberInfo
from nca47.objects import base
from nca47.objects import fields as object_fields


class Gmember(base.Nca47Object):
    VERSION = '1.0'

    fields = {
        'name': object_fields.StringField(),
        'gslb_zone_name': object_fields.StringField(),
        'ip': object_fields.StringField(),
        'port': object_fields.ListOfStringsField(),
        'enable': object_fields.StringField(),
        'gmember_id': object_fields.StringField(),
        'refcnt': object_fields.StringField(),
        'tenant_id': object_fields.StringField()
    }

    def __init__(self, context=None, **kwarg):
        self.db_api = db_api.get_instance()
        super(Gmember, self).__init__(context=None, **kwarg)

    @staticmethod
    def _from_db_object(dns_gmember, db_dns_gmember):
        """Converts a database entity to a formal :class:`Gmember` object.

        :param dns_gmember: An object of :class:`Gmember`.
        :param db_dns_gmember: A DB model of a Gmember.
        :return: a :class:`Gmember` object.
        """
        for field in dns_gmember.fields:
            dns_gmember[field] = db_dns_gmember[field]

        dns_gmember.obj_reset_changes()
        return dns_gmember

    def create(self, context, values):
        zone = self.db_api.create(GmemberInfo, values)
        return zone

    def update(self, context, id, values):
        record = self.db_api.update_object(GmemberInfo, id, values)
        return record

    def delete(self, context, id):
        record = self.db_api.delete_object(GmemberInfo, id)
        return record

    def get_objects(self, context, **values):
        record = self.db_api.get_objects(GmemberInfo, **values)
        return record

    def get_object(self, context, **values):
        record = self.db_api.get_object(GmemberInfo, **values)
        return record

    def get_all_object(self, str_sql):
        record = self.db_api.get_all_object(GmemberInfo, str_sql)
        return record

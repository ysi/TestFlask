#!/opt/homebrew/bin/python3.9
# coding=utf-8

from .entity import Entity
from .transportzone import TZSchema
from marshmallow import Schema, fields

class Segment(Entity):
    type = ''
    segment_type = ''
    admin_state = ''
    vlan_ids = []
    admin_state = ''
    connectivity = ''
    transportzone = ''
    vni = ''
    replication_mode = ''

    def __init__(self, name, id, unique_id):
        Entity.__init__(self)
        self.name = name
        self.id = id
        self.unique_id = unique_id

class SegmentSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    unique_id = fields.Str()
    type = fields.Str()
    replication_mode = fields.Str()
    admin_state = fields.Str()
    connectivity = fields.Str()
    segment_type = fields.Str()
    transportzone_obj = fields.Nested(TZSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

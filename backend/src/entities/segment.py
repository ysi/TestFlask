#!/opt/homebrew/bin/python3.9
# coding=utf-8

from .entity import Entity
from ..lib import nsxconnection
from marshmallow import Schema, fields

class Segment(Entity):
    type = ''
    segment_type = ''
    admin_state = ''
    vlan_ids = []
    admin_state = ''
    connectivity = ''
    transportzone = ''
    transportzone_obj = ''
    vni = ''
    replication_mode = ''

    def __init__(self, name, id, unique_id):
        Entity.__init__(self)
        self.name = name
        self.id = id
        self.unique_id = unique_id

    def show(self):
        print('Segment Informations: ' + self.name)
        print(' - id: ' + self.id)
        print(' - unique_id: ' + self.unique_id)
        print(' - segment_type: ' + self.segment_type)
        print(' - type: ' + self.type)
        print(' - vlans: ' + ', '.join(self.vlan_ids))
        print(' - vni: ' + self.vni)
        print(' - replication_mode: ' + self.replication_mode)
        print(' - admin_state: ' + self.admin_state)
        print(' - connectivity: ' + self.connectivity)
        print(' - transportzone: ' + self.transportzone)
        print(' - created_at: ' + str(self.created_at))
        print(' - updated_at: ' + str(self.updated_at))

class SegmentSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    unique_id = fields.Str()
    type = fields.Str()
    replication_mode = fields.Str()
    admin_state = fields.Str()
    connectivity = fields.Str()
    segment_type = fields.Str()
    transportzone = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

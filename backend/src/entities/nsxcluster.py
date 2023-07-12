#!/opt/homebrew/bin/python3.9
# coding=utf-8

from .entity import Entity
from marshmallow import Schema, fields
from src.constants import constants


class NSXCluster(Entity):
    members = []
    online_node = []
    offline_node = []
    
    def __init__(self, id, status, overall_status):
        Entity.__init__(self)
        self.id = id
        self.status = status
        self.overall_status = overall_status


class NSXManager(Entity):
    def __init__(self, id, ip, fqdn, status):
        Entity.__init__(self)
        self.id = id
        self.ip = ip
        self.fqdn = fqdn
        self.status = status


class NSXManagerSchema(Schema):
    id = fields.Str()
    ip = fields.Str()
    fqdn = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class NSXClusterSchema(Schema):
    id = fields.Str()
    status = fields.Str()
    overall_status = fields.Str()
    online_node = fields.List(fields.Nested(NSXManagerSchema))
    offline_node = fields.List(fields.Nested(NSXManagerSchema))
    members = fields.List(fields.Nested(NSXManagerSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


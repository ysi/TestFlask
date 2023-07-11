#!/opt/homebrew/bin/python3.9
# coding=utf-8

from .entity import Entity
from marshmallow import Schema, fields

class TransportZone(Entity):

    def __init__(self, name, type, id, is_default, path):
        Entity.__init__(self)
        self.name = name
        self.type = type
        self.path = path
        self.id = id
        self.is_default = is_default

    def show(self):
        print('Transport Zone Informations: ' + self.name)
        print(' - id: ' + self.id)
        print(' - type: ' + self.type)
        print(' - path: ' + self.path)
        print(' - created_at: ' + str(self.created_at))
        print(' - updated_at: ' + str(self.updated_at))

class TZSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    type = fields.Str()
    is_default = fields.Str()
    path = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
        
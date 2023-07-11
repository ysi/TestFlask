#!/opt/homebrew/bin/python3.9
# coding=utf-8

from datetime import datetime
import uuid


class Entity():
    id = str(uuid.uuid1())

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

# -*- coding: utf-8 -*-
"""
Block API
It overrides functions for database management and rase exception 
but allow you to create first database.
"""

from web import http
from openerp.addons.web.controllers.main import Database, db_list
openerpweb = http

class Database_restrict(Database):
    @openerpweb.jsonrequest
    def create(self, req, fields):

        # check if it is not first installation - restrict!

        dblist = db_list(req)
        if len(dblist) > 0:
            raise Exception('Not allowed')

        return super(Database_restrict, self).create(req, fields)

    @openerpweb.jsonrequest
    def duplicate(self, req, fields):
        raise Exception('Not allowed')

    @openerpweb.jsonrequest
    def drop(self, req, fields):
        raise Exception('Not allowed')

    @openerpweb.httprequest
    def backup(self, req, backup_db, backup_pwd, token):
        raise Exception('Not allowed')

    @openerpweb.httprequest
    def restore(self, req, db_file, restore_pwd, new_db):
        raise Exception('Not allowed')

    @openerpweb.jsonrequest
    def change_password(self, req, fields):
        raise Exception('Not allowed')

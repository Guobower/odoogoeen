# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class oph_cim10(orm.Model):
    _name = 'oph.cim10'

    _columns = {
              'name':fields.char('Name', size = 64, help = ""),
              'code':fields.char('Code', size = 16, help = "Very short name"),
              'comment':fields.text('Comment')
              }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

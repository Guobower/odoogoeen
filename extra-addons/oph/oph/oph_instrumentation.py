# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
from datetime import datetime

class oph_instrumentation_type(osv.Model):
    """
    Type of instruments
    """

    _name = "oph.instrumentation.type"

    _columns = {
              'name':fields.char('Name', help = 'Name of the type', size = 32),
              'comment':fields.char('Comment', size = 128, help = 'Comment the type of instrument'),
              'instrumentation_ids':fields.one2many('oph.instrumentation', 'type_id', 'Instrumentation'),
              }

class oph_instrumentation(orm.Model):
    """
    Instrumentation object
    """
    _name = "oph.instrumentation"

    _columns = {
              'name':fields.char('Name', size = 64, help = 'Name of the instrument'),
              'model':fields.char('Model', size = 64, help = 'Model name'),
              'serial_number':fields.char('Serial Number', size = 64, help = 'serial number of the instrument'),
              'date_on': fields.date('Date', help = 'Start-up date'),
              'date_purchase':fields.date('Purchase Date', help = 'Start-up date'),
              'warranty':fields.char('Warranty', size = 64),
              'price':fields.integer('Price', help = 'Purchase Price'),
              'comment':fields.text('Comment'),
              'type_id':fields.many2one('oph.instrumentation.type', 'Instrumentation type')
              }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
from datetime import datetime


class oph_filling_template(orm.Model):
    _name = 'oph.filling.template'

    _columns = {
              'name':fields.char('Name', size = 64, help = "Meanfull name to resume purpose template"),
              'code':fields.char('Code', size = 16, help = "Very short name"),
              'as_od':fields.text('AS_OD'),
              'ps_od':fields.text('PS_OD'),
              'as_os':fields.text('AS_OS'),
              'ps_os':fields.text('PS_OS'),
              'comment':fields.char("Comment", size = 128),
              'measurement_ids':fields.one2many('oph.measurement', 'filling_template_id', 'Measurement'),
              }

class oph_measurement(orm.Model):
    _inherit = 'oph.measurement'

    def on_change_template_id(self, cr, uid, ids, template_id, context = None):
        print "ON_CHANGE_TEMPLATE_ID"
        obj_filling_template = self.pool.get('oph.filling.template').browse(cr, uid, template_id, context = context)
        return {'value':{
                          'as_od':obj_filling_template.as_od,
                          'as_os':obj_filling_template.as_os,
                          'ps_od':obj_filling_template.ps_od,
                          'ps_os':obj_filling_template.ps_os,
                          }
                 }

        #=======================================================================
        # return { 'value':
        #                { 'event_col_1': temp.col_1,
        #                  'event_col_2': temp.col_2}
        #     }
        #=======================================================================

    _columns = {
                'filling_template_id':fields.many2one('oph.filling.template', 'Filling Template'),
              }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

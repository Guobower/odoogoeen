# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _

class oph_appointment_memo(osv.osv_memory):
    _name = "oph.appointment.memo"
    _description = "Appointment Memo Factory"

    _columns = {
              'date': fields.date('Statement Date', required = True, help = "Date of the current day to print on report"),
              'product_id': fields.many2one('product.product', 'Product', domain = [('sale_ok', '=', True)], change_default = True),
              }

    _defaults = {
               'date': lambda *a: time.strftime('%Y-%m-%d'),
               }

    def print_appointment_memo(self, cr, uid, ids, context = None):
        print "JE PASSE PAR PRINY8APPOINTMENT8MEMO"
        if context is None:
            context = {}

        active_ids = context.get('active_ids')

        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        data = self.read(cr, uid, ids, context = context)[0]

        context['date_report'] = data.get('date')
#        context['molecule'] = data.get('molecule', '')[1]
#        context['indication'] = data.get('indication', '')[1]
        # import pdb;pdb.set_trace()

        datas = {
           'ids':active_ids,
           'model':'crm.meeting',
           'form':data,
           'context':context,
           }

        return {
            'type': 'ir.actions.report.xml',
            'report_name':'oph.appointment.memo',
            'datas':datas,
            'context':context
            }

oph_appointment_memo()

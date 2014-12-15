# -*- coding: utf-8 -*-
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _

class oph_ivt_prescription(osv.osv_memory):
    _name = "oph.ivt.prescription"
    _description = "IVT Prescription Factory"

    _columns = {
              # 'name': fields.char('Molecule', size = 128, required = True),
              'date': fields.date('Statement Date', required = True, help = "Date of the current day to print on report"),
              # 'molecule':fields.char('Molecule', size = 64),
              'molecule':fields.many2one('oph.brandname', 'Brandname', domain = "[('ivt','=',True)]"),
              'indication':fields.many2one('oph.indication', 'Indication', domain = "[('ivt','=',True)]"),
              }

    _defaults = {
               'date': lambda *a: time.strftime('%Y-%m-%d'),
               }

    def print_ivt_prescription(self, cr, uid, ids, context = None):
        if context is None:
            context = {}

        active_ids = context.get('active_ids')

        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        data = self.read(cr, uid, ids, context = context)[0]

        context['date_report'] = data.get('date')
        context['molecule'] = data.get('molecule', '')[1]
        context['indication'] = data.get('indication', '')[1]
        # import pdb;pdb.set_trace()

        datas = {
           'ids':active_ids,
           'model':'oph.bloc.agenda.line',
           'form':data,
           'context':context,
           }

        return {
            'type': 'ir.actions.report.xml',
            'report_name':'oph.ivt.prescription',
            'datas':datas,
            'context':context
            }

oph_ivt_prescription()

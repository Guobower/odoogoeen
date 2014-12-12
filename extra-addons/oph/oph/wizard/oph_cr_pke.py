# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.osv import osv, fields
from openerp.tools.translate import _

class oph_cr_pke(osv.osv_memory):
    _name = "oph.cr.pke"
    _description = "Report for CROP PKE"  # don't forget u for unicode char in the string value u"Rapport personnalisé"

    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'date': fields.date('Prescription Date', required = True, help = "Date or the current day to print on report"),
        'var0': fields.integer('VAR0'),
        'var1': fields.integer('VAR1'),
        'var2': fields.integer('VAR2'),
        'bool0':fields.boolean('BOOL0'),
        'bool1':fields.boolean('BOOL1'),
        }

    _defaults = {
                 'date': lambda *a: time.strftime('%Y-%m-%d'),
                }

    def action_cancel(self, cr, uid, ids, context = None):
        """
        Close Etat Factory form
        Je n'ai pas encore trouvé la différence en ne mettant pas cette méthode.
        A quoi sert cette méthode par rapport à rien?
        """
        print "PASSING IN ACTION_CANCEL"
        return {'type':'ir.actions.act_window_close'}

    def print_report(self, cr, uid, ids, context = None):
        print " PASSING IN PRINT_STATEMENT. CONTEXT IS:", context
        if context is None:
            context = {}
        active_ids = context.get('active_ids')
        print "ACTIVE_IDS :%s" % active_ids
        print "CONTEXT: %s" % context
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        data = self.read(cr, uid, ids, context = context)[0]
        print "NAME:%s; DATE:%s; TEMPLATE:%s;" % (data['name'], data['date'], data['hba1c'],)
        #=======================================================================
        context['date_report'] = data['date']
        # context['ref_statement'] = data['name']
        # context['mention']='Document original à conserver."

        # template = data['template']
        #=======================================================================

        modele = 'diabetic.report'  # modele par defaut


        meeting_obj = self.pool.get('crm.meeting')
        data = meeting_obj.read(cr, uid, active_ids[0], context = context)
        print "DATA:%s" % data
        datas = {
             'ids': active_ids,
             'model': 'crm.meeting',
             'form': data,
             'context': context,
                    }
#===============================================================================
# # To write in account.invoice the ref_statement from the popup wizard
#         table = self.pool.get('account.invoice')
#         for id in datas['ids']:
#             table.write(cr, uid, id, {'ref_statement': context.get('ref_statement', 'May be you forget something')})
#===============================================================================

        return {
            'type': 'ir.actions.report.xml',
            'report_name': modele,
            'datas': datas,
            'context': context,
        }

oph_diabetic_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


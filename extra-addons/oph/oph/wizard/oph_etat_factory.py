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

class oph_etat_factory(osv.osv_memory):
    _name = "oph.etat.factory"
    _description = "Custom report"  # don't forget u for unicode char in the string value u"Rapport personnalisé"

    _columns = {
        'name': fields.char('Statement Ref', size = 128, required = True),
        'date': fields.date('Statement Date', required = True, help = "Date of the current day to print on report"),
        'template': fields.selection(
                                     (('LM', 'Longue Maladie'),
                                      ('NORD', 'AMG NORD'),
                                      ('SUD', 'AMG SUD'),
                                      ('ILES', 'AMG ILES'),
                                      ('AT', 'Accident de Travail'),
                                      ('SMIT', 'SMIT')),
                                      "Template", help = 'Choix du modele de report'),
      }
    _defaults = {
        'name': 'xxxLM, xxxNORD, xxxSUD, xxxSUD, xxxAT',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'template': 'LM',
      }

    def action_cancel(self, cr, uid, ids, context = None):
        """
        Close Etat Factory form
        Je n'ai pas encore trouvé la différence en ne mettant pas cette méthode.
        A quoi sert cette méthode par rapport à rien?
        """
        print "PASSING IN ACTION_CANCEL"
        return {'type':'ir.actions.act_window_close'}

    def print_statement(self, cr, uid, ids, context = None):
        if context is None:
            context = {}

        active_ids = context.get('active_ids')

        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}

        data = self.read(cr, uid, ids, context = context)[0]

        context['date_report'] = data['date']
        context['ref_statement'] = data['name']
        template = data['template']

        modele = 'account.invoice.lm'  # modele par defaut
        # choix du template pour le report etat factory
        if template == 'SUD':
           modele = 'account.invoice.sud'
        elif template == 'SMIT':
           modele = 'account.invoice.smit'
        elif template == 'ILES':
           modele = 'account.invoice.iles'
        elif template == 'AT':
           modele = 'account.invoice.at'
        elif template == 'NORD':
           modele = 'account.invoice.nord'

        invoice_obj = self.pool.get('account.invoice')
        data = invoice_obj.read(cr, uid, active_ids[0], context = context)
        datas = {
             'ids': active_ids,
             'model': 'account.invoice',
             'form': data,
             'context': context,
                    }
# To write in account.invoice the ref_statement from the popup wizard
        table = self.pool.get('account.invoice')
        for id in datas['ids']:
            table.write(cr, uid, id, {'ref_statement': context.get('ref_statement', 'May be you forget something')})

        return {
            'type': 'ir.actions.report.xml',
            'report_name': modele,
            'datas': datas,
            'context': context,
        }

#    def print_etat(self, cr, uid, ids, context = None):
#        """
#        To put the value of ref_etat in the ref_etat field of records
#        """
#        print "Je PASSE DANS PRINT_ETAT DU WIZARD ETAT FACTORY"
#        print "AND CONTEXT is:", context
#        if context is None:
#            context = {}
#        datas = {'ids':context.get('active_ids', False)}
#        print "DATAS:", datas
#        if not datas:
#            return {'type': 'ir.actions.act_window_close'}
#        res = self.read(cr, uid, ids, ['name', 'date'], context = context)
#        res = res and res[0] or {}
#        datas['form'] = res
#
#        obj_invoice = self.pool.get('account.invoice')
#        for id in datas['ids']:
#            print id, datas['form']['name']
#            obj_incoive.write(cr, uid, id, {'ref_etat':datas['form']['name']})
#        return {
#            'datas':datas,
#                }
#===============================================================================
#    def print_etat(self, cr, uid, ids, context=None):
#        """
#        To get the date and print the report
#        @return : return report
#        """
#        if context is None:
#            context = {}
#        datas = {'ids': context.get('active_ids', [])}
#         res = self.read(cr, uid, ids, ['name', 'date', 'template',], context=context)
#        res = res and res[0] or {}
#        datas['form'] = res
#
# #choix du template pour le report
#        if datas['form']['template'] == 'LM':
#            modele='account.invoice.lm'
#        if datas['form']['template'] == 'SUD':
#            modele = 'account.invoice.sud'
#        if datas['form']['template'] == 'SMIT':
#            modele = 'account.invoice.smit'
#        if datas['form']['template'] == 'ILES':
#            modele = 'account.invoice.iles'
#        if datas['form']['template'] == 'AT':
#            modele = 'account.invoice.at'
#        if datas['form']['template'] == 'NORD':
#            modele = 'account.invoice.nord'
#
#        table = self.pool.get('account.invoice')
#        for id in datas['ids']:
#            table.write(cr, uid, id, {'ref_etat': datas['form']['name']})
# #
# # # Cela ne boucle pas sur records.
# # #        for record in self.browse(cr, uid, ids):
# # #            cr.execute(
# # #                       """UPDATE account_invoice SET x_ref_etat=%s WHERE id=%s""",
# # #                       ('BINGO', record.id)
# # #                       )
#        return {
#            'type': 'ir.actions.report.xml',
#            'report_name': modele, #'account.factory.etat.report',
#            'datas': datas,
#                }
#===============================================================================


oph_etat_factory()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


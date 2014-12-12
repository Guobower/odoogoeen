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

class oph_formula_prescription(osv.osv_memory):
    _name = "oph.formula.prescription"
    _description = "Formula report prescription"  # don't forget u for unicode char in the string value u"Rapport personnalisé"

    def _get_sel_template(self, cr, uid, context = None):
        return (
                ('SV', _('Single Vision')),
                ('SV-SG', _('Single Vision - Sun Glass')),
                ('MF', _('Multifocal')),
                ('MF-SG', _('Multifocal - Sun Glass')),
                ('BF', _('Bi-Focal')),
                ('BF-SG', _('Bi-Focal - Sun Glass')),
                ('RG', _('Reading Glasses')),
                )

    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'date': fields.date('Prescription Date', required = True, help = "Date or the current day to print on report"),
        'template': fields.selection(_get_sel_template, 'Template', help = "Select template"),
        }
    _defaults = {
        'name': 'Refraction',
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'template': 'MF-SG',
      }

    def action_cancel(self, cr, uid, ids, context = None):
        """
        Close Etat Factory form
        Je n'ai pas encore trouvé la différence en ne mettant pas cette méthode.
        A quoi sert cette méthode par rapport à rien?
        """
        print "PASSING IN ACTION_CANCEL"
        return {'type':'ir.actions.act_window_close'}

    def print_formula(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids')
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        data = self.read(cr, uid, ids, context = context)[0]
        context['date_report'] = data['date']
        #=======================================================================
        # # context['ref_statement'] = data['name']
        # # context['mention']='Document original à conserver."
        #=======================================================================
        template = data['template']
        modele = 'single.vision.report'  # modele par defaut
        # choix du template pour le report etat factory
        # modele == field name='report_name' du record des reports aeroo.
        if template == 'SV':
            modele = 'single.vision.report'
        if template == 'SV-SG':
           modele = 'single.vision.sunglasses.report'
        elif template == 'MF':
           modele = 'multifocal.report'
        elif template == 'MF-SG':
           modele = 'multifocal.sunglasses.report'
        elif template == 'BF':
           modele = 'bifocal.report'
        elif template == 'BF-SG':
           modele = 'bifocal.sunglasses.report'
        elif template == 'RG':
           modele = 'reading.report'

        meeting_obj = self.pool.get('crm.meeting')
        # import pudb;pudb.set_trace()
        data = meeting_obj.read(cr, uid, active_ids[0], context = context)
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

oph_formula_prescription()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


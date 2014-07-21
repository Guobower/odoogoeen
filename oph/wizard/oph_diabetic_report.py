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

class oph_diabetic_report(osv.osv_memory):
    _name = "oph.diabetic.report"
    _description = "Report for diabetic patient"  # don't forget u for unicode char in the string value u"Rapport personnalisé"

    def _get_default_receiver(self, cr, uid, context = None):
        active_ids = context.get('active_ids')
        obj = self.pool.get('crm.meeting')
        br = obj.browse(cr, uid, active_ids[0])
        res = br.partner_id.partner_ids[0].id  # on retourne l'id du premier de la liste.
        from pdb import set_trace
        set_trace()
        return res

    def _get_default_receiver_infos(self, cr, uid, context = None):
        active_ids = context.get('active_ids')
        obj = self.pool.get('crm.meeting')
        br = obj.browse(cr, uid, active_ids[0])
        res = br.partner_id.partner_ids[0].id  # on retourne l'id du premier de la liste.


    _columns = {
        'name': fields.char('Name', size = 128, required = True),
        'date': fields.date('Prescription Date', required = True, help = "Date or the current day to print on report"),
        'hba1c': fields.integer('HbA1c'),
        # 'receiver':fields.selection(_receiver_get, 'Receiver', help = 'Select the receiver for address in the report'),
        'receiver': fields.many2one('res.partner', 'Receiver', domain = [('colleague', '=', 'True')], help = "select the receiver of the report"),
        'receiver_title':fields.char('Receiver title', size = 8),
        'receiver_name':fields.char('Receiver name', size = 32),
        'receiver_street':fields.char('Receiver street', size = 32),
        'receiver_street2':fields.char('Receiver street2', size = 32),
        'receiver_city':fields.char('Receiver city', size = 32),
        'receiver_zip':fields.char('Receiver zip', size = 32),
        'receiver_bp':fields.char('Receiver bp', size = 32),
        }

    _defaults = {
                 'date': lambda *a: time.strftime('%Y-%m-%d'),
                 'hba1c': False,  # ca marche pas.
                 'receiver': _get_default_receiver
                }

    def action_cancel(self, cr, uid, ids, context = None):
        """
        Close Etat Factory form
        Je n'ai pas encore trouvé la différence en ne mettant pas cette méthode.
        A quoi sert cette méthode par rapport à rien?
        """
        return {'type':'ir.actions.act_window_close'}

    def print_report(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids')
        if not active_ids:
            return {'type': 'ir.actions.act_window_close'}
        data = self.read(cr, uid, ids, context = context)[0]
        print "DATA:%s" % data
        #=======================================================================
        context['date_report'] = data['date']
        context['hba1c'] = data['hba1c']
        context['receiver_title']=data['receiver_title']
        context['receiver_name']=data['receiver_name']
        

        # template = data['template']
        # context['mention']='Document original à conserver."context['receiver'] = data['receiver']
        #=======================================================================
        #
        #=======================================================================
        #=======================================================================
        modele = 'diabetic.report'

        meeting_obj = self.pool.get('crm.meeting')
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


oph_diabetic_report()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


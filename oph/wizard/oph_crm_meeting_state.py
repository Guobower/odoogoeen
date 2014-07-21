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
from openerp.osv import osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import pooler


class oph_crm_meeting_draft(osv.osv_memory):
    """
    This wizard will set to draft the all selected crm meeting records
    so after if you want you can delete them
    """

    _name = "oph.crm.meeting.draft"
    _description = "Set to draft the selected crm.meeting"

    def crm_meeting_draft(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        data_inv = pool_obj.get(context.get('active_model')).read(cr, uid, context['active_ids'], ['state'], context = context)  # return dict [{'state':u'str,'id':3245};{},...]
        for record in data_inv:
            pool_obj.get(context.get('active_model')).write(cr, uid, record['id'], {'state':'draft'}, context = context)
        return {'type': 'ir.actions.act_window_close'}

oph_crm_meeting_draft()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# There an example of that in account_invoice_state.py and account_invoice_state_view.xml

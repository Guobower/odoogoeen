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

class oph_account_voucher_deposit(osv.osv_memory):
    """
    This wizard will set the check_deposit field to True if 
    deposit
    """

    _name = "oph.account.voucher.deposit"
    _description = "Set the check_deposit to True"

    def account_voucher_deposit(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        modele = 'bdxcheck'

        pool_obj = pooler.get_pool(cr.dbname)
        data_inv = pool_obj.get(context.get('active_model')).read(cr, uid, context['active_ids'], ['journal_id'], context = context)

        journal_obj = self.pool.get('account.journal')
        for rec in data_inv:
            res = journal_obj.read(cr, uid, rec.get('journal_id')[0], ['name'], context = context)
            if res.get('name') != u'Chèques':
                # from pdb import set_trace
                # set_trace()
                raise osv.except_osv(_('Error!'), _('Cannot Deposit a %s! Please Cancel and Select again') % (res.get('name'),))

#         from pdb import set_trace
#         set_trace()

        for record in data_inv:
            pool_obj.get(context.get('active_model')).write(cr, uid, record['id'], {'check_deposit':True}, context = context)
        data = self.pool.get('account.voucher').read(cr, uid, context.get('active_ids')[0], context = context)
        datas = {
               'ids':context.get('active_ids'),
               'model':'account.voucher',
               'form':data,
               'context':context,
               }
        return {
                'type':'ir.actions.report.xml',
                'report_name':modele,
                'datas':datas,
                'context':context
                }

oph_account_voucher_deposit()

# for
#

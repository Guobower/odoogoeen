# -*- coding: utf-8 -*-
#===============================================================================
# Custom res_users object
# Add Etablissment payeur and Titulaire du cheque
#===============================================================================
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_voucher(orm.Model):
    """
    Custom account_voucher object (== Payment)
    Add field chq_owner
    For bank use ref payment instead
    """
    _inherit = "account.voucher"

    _columns = {
                'check_owner':fields.char('Check Owner', help = 'Owner of the check. Change it, if different of the customer"', size = 32),
                'check_deposit':fields.boolean('Check Deposit', help = 'Check Deposit'),
                }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

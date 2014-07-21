# -*- coding: utf-8 -*-
#===============================================================================
# Custom res_users object
# Add Etablissment payeur and Titulaire du cheque
#===============================================================================
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_voucher(orm.Model):
    """
    Custom account_voucher object
    Add field chq_owner
    Not usefull use memo and ref payment instead
    """
    _inherit = "account.voucher"

    #===========================================================================
    # def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context = None):
    #     """
    #     set the check_owner to be
    #     same as partner_id name by default
    #     An other exemple for using super is in onchange_date in oph_agenda.py
    #     Strangely res is not a dict but a bool on first so send an error msg
    #     but after the error it's the dict as espected.
    #     In onchange_date of oph_agenda.py res is a dict
    #     """
    #     print "IN ONCHANGE JOURNAL"
    #     res = super(account_voucher, self).onchange_journal(cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context = context)
    #     print "TYPE RES: %s" % (type(res),)
    #     partner_obj = self.pool.get('res.partner')
    #     import pdb;pdb.set_trace()
    #     br = partner_obj.browse(cr, uid, partner_id, context = None)
    #     res['value'].update({'check_owner' : br.name})
    #     return res
    #===========================================================================

    _columns = {
                'check_owner':fields.char('Check Owner', help = 'Owner of the check. Change it, if different of the customer"', size = 32),
                'check_deposit':fields.boolean('Check Deposit', help = 'Check Deposit'),
                }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

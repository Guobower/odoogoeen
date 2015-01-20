from openerp.osv import fields, osv, orm
from tools.translate import _


# --
class account_invoice(orm.Model):
    """
    Custom account.invoice(==Invoice)
    Add:
     payeur for paiement in New Caledonia
    ref_statement to ease bank reconciliation
    """
    _inherit = "account.invoice"

    _columns = {
        'payeur': fields.selection([
            ('CAFAT Mut', 'CAFAT Mutuelle'),
            ('SUD', 'AMG Sud'),
            ('NORD', 'AMG Nord'),
            ('ILES', 'AMG Iles'),
            ('LM', 'Longue Maladie'),
            ('AT', 'Accidents de travail'),
            ('SMIT', 'SMIT'),
            ('TM', 'Ticket moderateur'),
            ('BdC', 'Baie des Citrons')], 'Payeur'),  # required=True),
        'ref_statement': fields.char('Statement Ref', size = 32, help = 'Reference of the statement for bank reconcilation'),
        'date_acte':fields.date('Appointment Date')
        }

    def invoice_pay_customer(self, cr, uid, ids, context = None):
        """Set check owner to partner_id by default"""
        res = super(account_invoice, self).invoice_pay_customer(cr, uid, ids, context = context)
        print "IN CUSTOM INVOICE_PAY_CUSTOMER"
        partner_obj = self.pool.get('res.partner')
        br = partner_obj.browse(cr, uid, res['context']['default_partner_id'], context = None)
        res['context'].update({'default_check_owner' : br.name})
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

from osv import fields, osv
from openerp import netsvc

class sale_order(osv.Model):
    """
    This inherited class for going from quotation to
    invoice without any other step in the invoice workflow
    """
    _inherit = "sale.order"

    def action_button_confirm_to_invoice(self, cr, uid, ids, context = None):
        """Confirm the sale order, create an invoice and open the invoice form"""
        print "IN ACTION_BUTTON_CONFIRM_2_INVOICE"
        print "CONTEXT:%s" % (context,)
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        wf_service = netsvc.LocalService('workflow')
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'order_confirm', cr)
        return self.manual_invoice(cr, uid, ids, context = context)

    def onchange_shop_id(self, cr, uid, ids, shop_id, context = None):
        # import pdb;pdb.set_trace()
        v = {}
        if shop_id:
            shop = self.pool.get('sale.shop').browse(cr, uid, shop_id, context = context)
            if shop.project_id.id:
                v['project_id'] = shop.project_id.id
        return {'value': v}

    _columns = {'date_acte':fields.date('Date Acte'), }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

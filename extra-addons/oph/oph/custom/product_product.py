# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class product_product(orm.Model):
    """
    Custom product_product object
    Add field 'dilatation'
    Not usefull use memo and ref payment instead
    """
    _inherit = "product.product"

    _columns = {
                'dilatation':fields.boolean('Dilatation', help = 'Dilatation yes/no for this product'),
                }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

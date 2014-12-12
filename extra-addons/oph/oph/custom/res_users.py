# -*- coding: utf-8 -*-
#===============================================================================
# Custom res_users object
# Add an CAFAT ID for use in New Caledonia
#===============================================================================
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class res_users(orm.Model):
    """
    Custom res_users object
    Add a CAFAT ID for use in New Caledonia
    """
    _inherit = "res.users"
    _columns = {
                'cafat_id':fields.char('CAFAT ID', size = 16, help = 'CAFAT ID of the doctor = convention number. This is not the CAFAT Number as for a patient'),
                }

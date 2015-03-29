# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class oph_request(orm.Model):
    _name = 'oph.request'

    def on_change_oph_partner(self, cr, uid, ids, partner_id, date_request, context = None):
        if context is None:
            context = {}
        values = {}
        res_partner = self.pool.get('res.partner')
        # import pdb;pdb.set_trace()
        br = res_partner.browse(cr, uid, partner_id, context = None)
        name = 'Demande Accord' + ' ' + br.fullname + ' ' + date_request

        return {'value': {'name': name}}

    def request_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "open"}, context = context)
        return True

    def request_close(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "close"}, context = context)
        return True

    def request_cancel(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "cancel"}, context = context)
        return True

    def request_confirm(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "confirm"}, context = context)
        return True

    def _state_get(self, cr, uid, context = None):
        return [
                    ('draft', 'Draft'),
                    ('open', 'Open'),
                    ('confirm', 'Confirm'),
                    ('close', 'Close'),
                    ('cancel', 'Cancelled'),
                    ]

    def _priority_id_selection(self, cr, uid, context = None):
        tag_id_obj = self.pool.get('oph.todolist.tag')
        # tag_ids = tag_id_obj.search(cr, uid, [('default', '=', True), ], context = context)
        tag_ids = tag_id_obj.search(cr, uid, [], context = context)
        if tag_ids:
            res = tag_id_obj.read(cr, uid, tag_ids, ['name'], context = context)
            return [(str(r['id']), r['name']) for r in res]
        return True

    _columns = {
                'name':fields.char('Name', size = 128),
                'comment':fields.char('Comment', size = 128),
                'partner_id': fields.many2one('res.partner', 'Partner', change_default = True, required = True,),
                'referent_id':fields.many2one('res.partner', 'Referent', domain = [('colleague', '=', True)], required = True,),
                'request_line_ids':fields.one2many('oph.request.line', 'request_id', 'Accord Lines'),
                'date_request': fields.date('Request Date', readonly = True, states = {'draft':[('readonly', False)]}, select = True, help = "Keep empty to use the current date"),
                'state':fields.selection(_state_get, 'Status', select = True, readonly = True),
                'company_id': fields.many2one('res.company', 'Company', required = True, change_default = True, readonly = True, states = {'draft':[('readonly', False)]}),
                'priority_id':fields.selection(_priority_id_selection, 'Priority'),
                }

    _defaults = {
        'state': 'draft',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context = c),
        'date_request': lambda *a: time.strftime('%Y-%m-%d'),
                }

class oph_request_line(orm.Model):
    _name = 'oph.request.line'

    _columns = {
                'name':fields.char('Name', size = 16),
                'sequence': fields.integer('Sequence', help = "Gives the sequence of this line when displaying the invoice."),
                'request_id':fields.many2one('oph.request', 'Accord Reference', ondelete = "cascade", select = True),
                'product_id':fields.many2one('product.product', 'Product', select = True),
                'partner_id':fields.related('request_id', 'partner_id', type = 'many2one', relation = 'res.partner', string = 'Partner', store = True),
                'comment':fields.char('Comment', size = 128),
                }

class res_partner(orm.Model):
    """
     Inherits partner and adds invoice information in the partner form 
    """
    _inherit = 'res.partner'
    _columns = {
                'request_ids': fields.one2many('oph.request.line', 'partner_id', 'Accords CAFAT', readonly = True),
                }

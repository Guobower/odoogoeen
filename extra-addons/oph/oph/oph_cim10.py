# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class oph_cim10_category(osv.osv):

    def name_get(self, cr, uid, ids, context = None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context = context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context = None):
        res = self.name_get(cr, uid, ids, context = context)
        return dict(res)

    _name = "oph.cim10.category"
    _description = "CIM10 Chapter and Category"
    _columns = {
        'name': fields.char('Name', size = 64, required = True, translate = True, select = True),
        'complete_name': fields.function(_name_get_fnc, type = "char", string = 'Name'),
        'parent_id': fields.many2one('oph.cim10.category', 'Parent Category', select = True, ondelete = 'cascade'),
        'child_id': fields.one2many('oph.cim10.category', 'parent_id', string = 'Child Categories'),
        'sequence': fields.integer('Sequence', select = True, help = "Gives the sequence order when displaying a list of product categories."),
        'type': fields.selection([('view', 'View'), ('normal', 'Normal')], 'Category Type', help = "A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
        'parent_left': fields.integer('Left Parent', select = 1),
        'parent_right': fields.integer('Right Parent', select = 1),
    }


    _defaults = {
        'type' : lambda *a : 'normal',
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    def _check_recursion(self, cr, uid, ids, context = None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from product_category where id IN %s', (tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    ]
    def child_get(self, cr, uid, ids):
        return [ids]

oph_cim10_category()

class oph_cim10(orm.Model):
    _name = 'oph.cim10'

    _columns = {
              'name':fields.char('Name', size = 64, help = ""),
              'code':fields.char('Code', size = 16, help = "Very short name"),
              'comment':fields.text('Comment')
              }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

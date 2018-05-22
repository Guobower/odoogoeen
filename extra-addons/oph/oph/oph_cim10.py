# -*- coding: utf-8 -*-
import logging
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class oph_cim10_category(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id', 'code'], context=context)
        res = []
        # from pdb import set_trace; set_trace()
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
            if record['code']:
                name = record['code'] + ' / ' + name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "oph.cim10.category"
    _description = "CIM10 Chapter and Category"
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'code':fields.char('Code', size=16, required=True, translate=True, select=True),
        'description':fields.text('Description', translate=True),
        'parent_id': fields.many2one('oph.cim10.category', 'Parent Category', select=True, ondelete='cascade'),
        'child_id': fields.one2many('oph.cim10.category', 'parent_id', string='Child Categories'),
        'sequence': fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of product categories."),
        'type': fields.selection([('view', 'View'), ('normal', 'Normal')], 'Category Type', help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        }

    _defaults = {
        'type' : lambda *a : 'normal',
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    def _check_recursion(self, cr, uid, ids, context=None):
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

    def name_get(self, cr, uid, ids, context=None):
        """
        Returns the preferred display value (text representation) 
        for the records with the given ids. 
        By default this will be the value of the "name" column, 
        unless the model implements a custom behavior.
        
        @Return: type:list(tuple)
        @Returns: list of pairs (id,text_repr) for all records with the given ids.
        """
        _logger.info("In NAME_GET de L'OBJET OPH.CIM10")
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            # import pdb; pdb.set_trace()
            if record.code:
                name += ', ' + record.code
            res.append((record.id, name))
        return res

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    _columns = {
              'name':fields.char('Name', size=64, help="Long name"),
              'code':fields.char('Code', size=16, help="Very short name"),
              'categ_id': fields.many2one('oph.cim10.category', 'Category', required=True, change_default=True, domain="[('type','=','normal')]" , help="Select category for the current product"),
              'comment':fields.text('Comment'),
              'description':fields.text('Comment', translate=True),
              # image: all image fields are base64 encoded and PIL-supported
              'image': fields.binary("Image",
                                     help="This field holds the image used as image for the product, limited to 1024x1024px."),
              'image_medium': fields.function(_get_image, fnct_inv=_set_image,
                                              string="Medium-sized image", type="binary", multi="_get_image",
                                              store={'oph.cim10': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10), },
                                              help="Medium-sized image of the product. It is automatically "\
                                              "resized as a 128x128px image, with aspect ratio preserved, "\
                                              "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
              'image_small': fields.function(_get_image, fnct_inv=_set_image,
                                             string="Small-sized image",
                                             type="binary", multi="_get_image",
                                             store={'oph.cim10': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10), },
                                             help="Small-sized image of the product. It is automatically "\
                                                  "resized as a 64x64px image, with aspect ratio preserved. "\
                                                  "Use this field anywhere a small image is required."),
                'agenda.bloc.line_ids':fields.one2many('oph.bloc.agenda.line', 'cim10_id', string="CIM10 Codification", readonly=True),
                'oph.request.ids':fields.one2many('oph.request', 'cim10_id', string='CIM10 codification', readonly=True),
                }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

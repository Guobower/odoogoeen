# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _



class oph_evasan(orm.Model):
    """EVASAN REQUEST"""
    _name = 'oph.evasan'

    _columns = {
              'name':fields.char('Name', size = 32,),
              'partner_id':fields.many2one('res.partner', 'Partner',),
              'comment':fields.text('Comment'),
              'sent': fields.boolean('Sent', readonly = True, help = "It indicates that the invoice has been sent."),
              'user_id': fields.many2one('res.users', 'Salesperson', readonly = True, track_visibility = 'onchange', states = {'draft':[('readonly', False)]}),
              'company_id': fields.many2one('res.company', 'Company', required = True, change_default = True, readonly = True, states = {'draft':[('readonly', False)]}),
              # 'destination':
              # hospital
              # date_in
              # doctor
              # tel
              'motive':fields.text('Motive', help = 'motive for admission'),
              'CIM10':fields.char('CIM10', size = 32),
              'Diagnosis':fields.char('Diagnosis', size = 64),
              'seat':fields.boolean('Seat', help = 'patient can seat'),
              'stand':fields.boolean('Stand', help = 'patient can stand up'),
              'walk':fields.boolean('Walk', help = 'patient can walk'),
              'eat':fields.boolean('Eat', help = 'eat alone'),
              'weight':field.integer('Weight', help = 'Weight'),
              'transport': fields.selection([
            ('alone', 'Alone'),
            ('acc familial', 'Acc familial'),
            ('acc med', 'Acc médical'),
            ('acc paramed', 'Acc paramedical'),
            ('seat', 'Assis'),
            ('cancel', 'Cancelled'),
            ], 'Transportation', select = True, readonly = False, help = 'Modalité de transport'),

              }

    _defaults = {
        'user_id': lambda s, cr, u, c: u,
        'sent': False,
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context = c),
    }






# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

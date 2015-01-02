# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from openerp.osv import osv, fields, orm
from openerp.tools.translate import _

class oph_tag_agenda(orm.Model):
    _name='oph.tag.agenda'
    _columns={
              'name':fields.char('Name',size=16),
              'code':fields.char('Code',size=8),
              'duration':fields.integer('Duration',help ='Duration in minutes'),
              }
    
class oph_slot(orm.Model):
    """
    A simple slot
    for one appointment
    parameters: 
    -start_time qui est l'heure de début du crénaux. Il faudra voir pour le formatage 08:00:00, 08:00, 08h,08h00,8h
    -duration en float qui est la durée du crénaux.
    """
    _name='oph.slot'
    
    def onchange_tag(self,cr,uid,ids,context=None):
        #context.get['tag_id'] = l'id  de oph.tag.agenda que je veux
        if context is None:
            context={}
        print context.get('tag_id',False)
        res=self.pool.get('oph.tag.agenda')
        res=res.browse(cr,uid,context.get('tag_id',False),context=context) 
        print "res.duration:%s" %(res.duration,)
        #import pdb;pdb.set_trace()
        return {
               # 'warning': {'title': 'Error!', 'message': 'Something went wrong! Please check your data'},
                'value': {
                          'duration':res.duration},
                }

    _columns={
              'start_time':fields.char('Start Time', size=8),
              #'duration':fields.float('Duration'),
              'duration':fields.integer('Duration',help ='Duration in minutes'),
              'tag_id':fields.many2one('oph.tag.agenda','Tag',help='Set the type of the slot'),
              }
    #===========================================================================
    # 
    # _defaults={
    #            'duration':lambda s, cr, uid, c:s._get_default_duration(cr, uid, context = c),
    #            }
    #===========================================================================

class oph_day_template(orm.Model):
    """
    Journee type.
    par exemple : lundi consultation, lundi + actes techniques, mardi cs + fermé l'apres midi etc..., fermee toute la journee
    """
    _name='oph.day.template'
    
    
    
    _columns={
              'name':fields.char('Name', help='A simple name', size=32),
              'comment':fields.char('A small description', size=128),
              'slot_ids':fields.many2many('oph.slot','oph_slot_day_template_rel','day_template_id', 'slot_id', 'Slots'),
              }
    
    
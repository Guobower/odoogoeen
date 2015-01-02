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
from openerp.osv import osv, fields, orm
from openerp.tools.translate import _
import re

class oph_tag_agenda(orm.Model):
    """A tag for the slot
    
        You can create as many tags as you want
    """
    _name='oph.tag.agenda'

    def _get_status_agenda(self, cursor, user_id, context = None):
        return (
                # ('draft', 'Draft'),
                ('cs', 'Consultation'),
                ('tech', 'Technique'),
                # ('open', 'Open'),
                # ('busy', 'Busy'),
                ('close', 'Close'),
                # ('cancel', 'Cancel'),
                # ('no_show', 'No Show'),
                # ('wait', 'Wait'),
                # ('in', 'In'),
                # ('in_between', 'In Between'),
                # ('done', 'Out'),
                )

    _columns={
              'name':fields.char('Name',size=16),
              #'code':fields.char('Code',size=8),
              'duration':fields.integer('Duration',help ='Duration in minutes'),
              'state': fields.selection(_get_status_agenda, 'State', readonly = False),
              }

class oph_slot(orm.Model):
    """ A simple slot  for one appointment

        start_time : start hour
        duration; integer. in minutes
        tag_id:type of the slot
    """
    _name='oph.slot'
    
    def onchange_tag(self,cr,uid,ids,context=None):
        """Onchange method to get the default duration"""
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

    def onchange_check_format(self,cr,uid,id,start_time,context=None):
        """Check if start_time format is valid"""
        pattern=re.compile(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$')
        match=pattern.match(start_time)
        if context is None:
            context={}
        if match is None:
            return {
                        'warning': {'title': _('Error!'), 'message': _('Something went wrong! Please check your data. The data "start_time" must be hh:mm')},}
        else:
            return {}

    _columns={
              'start_time':fields.char('Start Time', size=8),
              'duration':fields.integer('Duration',help ='Duration in minutes'),
              'tag_id':fields.many2one('oph.tag.agenda','Tag',help='Set the type of the slot'),
              }

class oph_day_template(orm.Model):
    """Template for a day"""
    _name='oph.day.template'
    _columns={
              'name':fields.char('Name', help='A simple name', size=32),
              'comment':fields.char('A small description', size=128),
              'slot_ids':fields.many2many('oph.slot','oph_slot_day_template_rel','day_template_id', 'slot_id', 'Slots'),
              }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

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

class oph_slot(orm.Model):
    """
    A simple slot
    for one appointment
    parameters: 
    -start_time qui est l'heure de début du crénaux. Il faudra voir pour le formatage 08:00:00, 08:00, 08h,08h00,8h
    -duration en float qui est la durée du crénaux.
    """
    _name='oph.slot'
    _columns={
              'start_time':fields.char('Start Time', size=8),
              'duration':fields.float('Duration'),
              }
    
    
class oph_day_template(orm.Model):
    """
    TODO
    """
    _name='oph.day.template'
    
    _columns={
              'name':fields.char('Name', help='A simple name', size=32),
              'slot_ids':fields.many2many('oph.slot','oph_slot_day_template_rel','day_template_id', 'slot_id', 'Slots'),
              }
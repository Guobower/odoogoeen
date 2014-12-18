# -*- coding: utf-8 -*-

from tools.translate import _
from osv import osv, fields
from tools.translate import _
from datetime import datetime, timedelta
import pytz
import arrow
import inspect

class day_template_agenda_factory(osv.osv_memory):
    """
    TODO
    """
    _name = "day.template.agenda.factory"
    _description = "Agenda factory. Set up of slots using day template"

    def create_slot(self,cr,uid,ids,context=None):
        return {}
    
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
    
            
    _columns = {
                'name':fields.char('Name', size = 8, help = "Name for the open slots to be created"),
                'date':fields.date('Date', help = 'Day for slot to create'),
                'state': fields.selection(_get_status_agenda, 'State', readonly = False),
                'day_template_id':fields.many2one('oph.day.template','Day Template'),
                            }
    _defaults = {
                 'name': 'New Factory',
                }

day_template_agenda_factory()
# create(cr, user, vals, context=None)
# write(cr, user, ids, vals, context=None)¶

# Factory par 1/2 journée ou journée  TODO
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

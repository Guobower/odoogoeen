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
        """
        TODO
        """
        print "PASSING in %s. CONTEXT is: %s" % (inspect.stack()[0][3], context)
        #il y a pas grand chose dans le context
        res = self.read(cr, uid, ids, ['name','date', 'state','day_template_id',], context = None)
        print "RES:%s" %(res,)
        #récupérons le record day_template dont nous avons besoin
        print "day_template:%s" %(res[0]['day_template_id'],)
        #l'id du day_template que je veux est sous res[0]['day_template_id'][0] 
        daytemplate=self.pool.get('oph.day.template').browse(cr, uid, res[0]['day_template_id'][0], context = context)
        print "DAYTEMPLATE:%s" %(daytemplate)
        print "browse.name:%s" %(daytemplate.name,)
        print "browse.slot_ids:%s" %(daytemplate.slot_ids,)
        print "date:%s" %(res[0]['date'])
        agenda=self.pool.get('crm.meeting')
        for slot in daytemplate.slot_ids:
            print 'start,duration:%s-%s' %(slot.start_time,slot.duration,)
            start_date=res[0]['date']+' '+slot.start_time
            print 'start_date:%s' %(start_date,)
            vals={'date':start_date,'date_deadline':'2015-01-01 08:00:00'}
            agenda.create(cr,uid,vals,context=None)
            # c'est pas mal mais il faut faire des conversions en utc.
            #travail a faire sur le float time de duration.
        return {}
    
    def _get_status_agenda(self, cursor, user_id, context = None):
        return (
                ('cs', 'Consultation'),
                ('tech', 'Technique'),
                ('close', 'Close'),
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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-

from tools.translate import _
from osv import osv, fields
from tools.translate import _
from datetime import datetime, timedelta
import pytz
import arrow
import inspect

class day_template_agenda_factory(osv.osv_memory):
    """Wizard for agenda factory using the day template"""
    _name = "day.template.agenda.factory"
    _description = "Agenda factory. Set up of slots using day template"
    
    def To_Arrow(self,date,start_time,duration,context=None):
        """Get an arrow object from a date an a start_time string
        
        @param : date type:string format : YYYY-MM-DD
        @param start_time: type string format hh:mm
        
        @return: string  format : 'YYYY-MM-DD hh:mm' In UTC timezone unaware
        """
        if context is None:
            context = {}
        format='YYYY-MM-DD HH:mm'
        print "PASSING in : %s - CONTeXT is :%s" % (inspect.stack()[0][3], context)
        print "PARAM: date=%s - start_time=%s" % (date, start_time)
        datetime=date+' '+start_time
        print "DATETIME:%s" %(datetime,)
        #aw=arrow.get(datetime, 'YYYY-MM-DD HH:mm') #mais utc aware
        # et c'est pas ce que je veux je veux locale tz aware
        aw=arrow.get(datetime,format).replace(tzinfo = context.get('tz', None)).to('UTC')
        
        print "AW:%s" %(aw,)
        print "AW DEADLINE:%s" %(aw.replace(minutes=+duration))
        #now get a str from arrow
        print "RETURN:%s" %(aw.format('YYYY-MM-DD HH:mm:ss'),)
      
        return {
                'date':aw.format('YYYY-MM-DD HH:mm:ss'),
                'date_deadline':aw.replace(minutes=+duration).format('YYYY-MM-DD HH:mm:ss'),
                }
    
         
    def strdate2arrow(self, dt, hm = None, context = None):
        """Return an arrow object in UTC from a datetime
        
        :param dt: datetime.
        :type dt: string can be a string with or without time informations
        :param hm: time 
        :type hm: string can be "8" or "08" for 8h must be converted to a formated time "HH-mm-ss"
        :returns date wih time
        :rtype: arrow
        :example:
        
        strdate2arrow('2012-10-18, '08:30')
        <arrow
        """
        #=======================================================================
        # Est ce qu'un champ date subit une modification à cause des TZ
        # quand il est inséré dans la database.
        # si on veut utiliser le hm (HH:mm:ss)
        # Comme on récupère une string en UTC
        #
        #=======================================================================
        if context is None:
            context = {}
        print "PASSING in : %s - CONTeXT is :%s" (inspect.stack()[0][3], context)
        print "CONTEXT:%s" % context
        print "hm:%s" %(hm,)

        if hm:
            hm = dict(zip(['hour', 'minute'], [int(x) for x in hm.lstrip('0').split(':') ]))
            arw = arrow.get(dt).replace(hour = hm['hour'], minute = hm['minute']).replace(tzinfo = context.get('tz', None)).to('UTC')
            return arw
        else:
            return arrow.get(dt)

    def create_slot(self,cr,uid,ids,context=None):
        if context is None:
            context={}
        datas=self.read(cr,uid,ids,['name','date','day_template_id'],context=context)
        print "datas:%s" %(datas,)
        
        #day_template=self.pool.get('oph.day.template')
        #day_template=day_template.browse(cr,uid,context.get('day_template_id',False),context=context) ca marche tres bien
        day_template=datas[0].get('day_template_id')[0]
        day_template=self.pool.get('oph.day.template').browse(cr,uid,day_template,context=context)
        print day_template
        
        meeting=self.pool.get('crm.meeting')
        
        for slot in day_template.slot_ids:
            print "date:%s" %(datas[0].get('date'),)
            print "start_time:%s" %(slot.start_time,)
            print "duration:%s" %(slot.duration,)
            print "tag_id code:%s" %(slot.tag_id.code,)
            print "To_Arrow:%s" %(self.To_Arrow(datas[0].get('date'),slot.start_time,slot.duration, context=context),)
            print "create a record in crm.meeting"
            #je crée le dict des valeurs que je veux stocker dans crm.meeting
            vals={
                  'name':datas[0].get('name'),
                  'date':self.To_Arrow(datas[0].get('date'),slot.start_time,slot.duration, context=context).get('date'),
                  'duration':slot.duration,
                  'date_deadline':self.To_Arrow(datas[0].get('date'),slot.start_time,slot.duration, context=context).get('date_deadline'),
                  }
            print "VALS:%s" %(vals,)
            meeting.create(cr,uid,vals,context=context)
            print "========"
        return {}
        #import pdb;pdb.set_trace()
    
    def create_slotbis(self,cr,uid,ids,context=None):
        """
        TODO
        """
        print "PASSING in %s. CONTEXT is: %s" % (inspect.stack()[0][3], context)
        
        # get datas of the wizard window
        res = self.read(cr, uid, ids, ['name','date', 'state','day_template_id',], context = None)
        print "RES:%s" %(res,)
        #récupérons le record day_template dont nous avons besoin
        print "day_template:%s. Son ID: " %(res[0]['day_template_id'],res[0]['day_template_id'][0])
        #l'id du day_template que je veux est sous res[0]['day_template_id'][0] 
        daytemplate=self.pool.get('oph.day.template').browse(cr, uid, res[0]['day_template_id'][0], context = context)
        print "DAYTEMPLATE:%s" %(daytemplate)
        print "daytemplate.name:%s" %(daytemplate.name,)
        print "daytemplate.slot_ids:%s" %(daytemplate.slot_ids,)
        print "date:%s" %(res[0]['date'])
        agenda=self.pool.get('crm.meeting')
        for slot in daytemplate.slot_ids: # je boucle sur les slot (start_time et duration)
            print 'start and duration:%s-%s' %(slot.start_time,slot.duration,)
            start_date= self.To_Arrow(date,slot.start_time)
            print 'start_date:%s' %(start_date,)
        from pdb import set_trace; set_trace()
            #vals={'date':start_date,'date_deadline':'2015-01-01 08:00:00'}
            #agenda.create(cr,uid,vals,context=None)
            # c'est pas mal mais il faut faire des conversions en utc.
            #travail a faire sur le float time de duration.
        return {}

    _columns = {
                'name':fields.char('Name', size = 8, help = "Name for the open slots to be created"),
                'date':fields.date('Date', help = 'Day for slot to create'),
                #'state': fields.selection(_get_status_agenda, 'State', readonly = False),
                'day_template_id':fields.many2one('oph.day.template','Day Template'),
                            }
    _defaults = {
                 'name': 'New Factory',
                }

day_template_agenda_factory()
# create(cr, user, vals, context=None)
# write(cr, user, ids, vals, context=None)¶
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

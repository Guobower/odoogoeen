# -*- coding: utf-8 -*-

from tools.translate import _
from osv import osv, fields
from tools.translate import _
from datetime import datetime, timedelta
import pytz
import arrow
import inspect

class agenda_factory(osv.osv_memory):
    '''
    '''
    _name = "agenda.factory"
    _description = "Agenda factory. Set up of slots"  # Mise en place des crénaux"


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

    def onetotwodigit(self, hm):
        f = '0{0}'
        if len(hm) < 2:
            return f.format(*hm)
        else:
            return hm

    def complete(self, hm):
        """
        Return a complete hm with 
        HH:mm:ss 
        filling with 00 as necessary
        """
        while len(hm) < 3:
            hm.append('00')
        return hm

    def hm_format(self, hm):
        """
        format a string time to : HH:mm:ss
        """
        res = self.complete(map(self.onetotwodigit, hm.split(':')))
        res = ':'.join(res)  # convert list to string
        return res

    def shift(self, aw, step):
        """
        Skip aw ahead of step
        
        :param aw: arrow object
        :param step: integer (minutes)
        :returns: arrow object, step minutes later
        :rtype: arrow
        """
        return aw.replace(minutes = +step)

    def onchange_start(self, cr, uid, ids, hm, context = None):
        """
        TODO Pourquoi il n'y pas de changement dans les views
        
        """
        # print "ONCHANGE_START"
        if context is None:
            context = {}
        res = {'values':{}}
        res['values'] = {
                       'start_h':self.hm_format(hm),
                       }
        # print "RES:%s" % res
        return res

    def onchange_end(self, cr, uid, ids, hm, context = None):
        """
        TODO Pourquoi il n'y pas de changement dans les views
        """
        # print "ONCHANGE_END"
        if context is None:
            context = {}
        res = {'values':{}}
        res['values'] = {'end_h':self.hm_format(hm),
                         }
        # print "RES:%s" % res
        return res

    def strdate2arrow(self, dt, hm = None, context = None):
        """
        Return an arrow object in UTC
        
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
        print "STR2ARROW"
        print "CONTEXT:%s" % context

        if hm:
            hm = self.hm_format(hm)
            hm = dict(zip(['hour', 'minute'], [int(x) for x in hm.lstrip('0').split(':') ]))
            arw = arrow.get(dt).replace(hour = hm['hour'], minute = hm['minute']).replace(tzinfo = context.get('tz', None)).to('UTC')
            return arw
        else:
            return arrow.get(dt)

    def strdate2arrow_bis(self, dt, hm = None, context = None):
        """
        Return an arrow object in UTC
        
        :param dt: datetime
        :type dt: string
        :param hm: time 
        :type hm: string can be "8" or "08" for 8h must be converted to a formated time "HH-mm-ss"
        :returns date wih time
        :rtype: arrow
        :example:
        
        strdate2arrow('2012-10-18, '08:30')
        <arrow
        
        .. note if context is None the return arrow is in 'UTC'
        """
        if context is None:
            context = {}
        if hm:
            hm = dict(zip(['hour', 'minute'], [int(x) for x in hm.lstrip('0').split(':') ]))
            arw = arrow.get(dt).replace(hour = hm['hour'], minute = hm['minute']).replace(tzinfo = context.get('tz', None)).to('UTC')
            return arw
        else:
            return arrow.get(dt)

    def make_slots(self, rec, fmt = 'YYYY-MM-DD HH:mm:ss'):
        """
        Make the slots as arrow object
        
        :param rec: record from database 
        :type rec: dictionnary
        .. warning:: rec must have the 'start' and 'stop' and 'step' keys
        :param fmt: formatting string
        .. note:: fmt is always 'YYYY-MM-DD HH:mm:ss'
        :type fmt: str
        :return an iterable of the start and stop datetime for the slots.
        :rtype list of tuple
        
        :example:
        
        make_slots({'start':'2013-10-18 08:30:00', 'stop':'2013-10-18 10:00:00','step':15})
        [(<Arrow [2013-10-18T08:30:00+00:00]>, <Arrow [2013-10-18T08:45:00+00:00]>), 
        (<Arrow [2013-10-18T08:45:00+00:00]>, <Arrow [2013-10-18T09:00:00+00:00]>), 
        (<Arrow [2013-10-18T09:00:00+00:00]>, <Arrow [2013-10-18T09:15:00+00:00]>), 
        (<Arrow [2013-10-18T09:15:00+00:00]>, <Arrow [2013-10-18T09:30:00+00:00]>), 
        (<Arrow [2013-10-18T09:30:00+00:00]>, <Arrow [2013-10-18T09:45:00+00:00]>), 
        (<Arrow [2013-10-18T09:45:00+00:00]>, <Arrow [2013-10-18T10:00:00+00:00]>)]
        """
        l = list()
        ll = list()

        for key in ['start', 'stop']:
            val = arrow.get(rec[key], fmt)
            rec[key] = val
        while (rec['start'] < rec['stop']):
            l.append(rec['start'])
            rec['start'] = self.shift(rec['start'], rec['step'])
            ll.append(rec['start'])
        return zip(l, ll)

    def create_slot(self, cr, uid, ids, context = None):
        """
#     Create slots crm.meeting meeting
# 
#     step: slot duration
#      """
        print "PASSING in %s / CONTEXT:%s" % (inspect.stack()[0][3], context)

        fmt = 'YYYY-MM-DD HH:mm:ss'
        l = list()
        ll = list()
        if context is None:
            context = {}
        res = self.read(cr, uid, ids, ['date', 'start_dt', 'stop_dt', 'step', 'ampm', 'start_h', 'end_h', 'day_on', 'day_off', 'name', 'state'], context = None)

        # creation des slots à partir de start et stop qui sont des datetimes.
        # avec read on récupère  une liste de dictionnaire
        # les datetimes sont en utc.
        # les date retournée par read on l'air d'etre des str de la forme YYYY-MM-DD
        res = res[0]  # seul le premier enregistrement nous intéresse
        print "RES", res
        # from pdb import set_trace
        # set_trace()  # --
        if res['ampm'] == 'afternoon' or res['ampm'] == 'morning':
            for key in ('start_h', 'end_h'):
                dt = res['date'] + ' ' + self.hm_format(res[key])
                val = arrow.get(dt, fmt).replace(tzinfo = context.get('tz', None)).to('UTC')
                res[key] = val  # récupére les datetime pour en faire des arrow obj et les injecte dans le dictionnaire.
            while (res['start_h'] < res['end_h']):
                l.append(res['start_h'])
                res['start_h'] = self.shift(res['start_h'], res['step'])
                ll.append(res['start_h'])
            p = zip(l, ll)
            for (begin, end) in p:
                if res['state'] in ['cs', 'tech']:
                    tag = res['state']
                else:
                    tag = False
                self.pool.get('crm.meeting').create(cr, uid, {'date':begin, 'date_deadline':end, 'name':res['name'], 'state':res['state'], 'tag':tag}, context = None)
        # --
        elif (res['ampm'] == 'daylong'):
            for key in ('day_on', 'day_off', 'start_h', 'end_h'):
                dt = res['date'] + ' ' + self.hm_format(res[key])
                val = arrow.get(dt, fmt).replace(tzinfo = context.get('tz', None)).to('UTC')
                res[key] = val
            # -- morning
            while (res["day_on"] < res['start_h']):
                l.append(res['day_on'])
                res['day_on'] = self.shift(res['day_on'], res['step'])
                ll.append(res['day_on'])
            p = zip(l, ll)
            for (begin, end) in p:
                if res['state'] in ['cs', 'tech']:
                    tag = res['state']
                else:
                    tag = False
                print "TAG:%s" % (tag,)
                self.pool.get('crm.meeting').create(cr, uid, {'date':begin, 'date_deadline':end, 'name':res['name'], 'state':res['state'], 'tag':tag}, context = None)

            l = list()
            ll = list()
            while (res["end_h"] < res['day_off']):
                l.append(res['end_h'])
                res['end_h'] = self.shift(res['end_h'], res['step'])
                ll.append(res['end_h'])
            p = zip(l, ll)
            for (begin, end) in p:
                print "RES['state']: %s" % (res['state'],)
                if res['state'] in ['cs', 'tech']:
                    tag = res['state']
                else:
                    tag = False
                self.pool.get('crm.meeting').create(cr, uid, {'date':begin, 'date_deadline':end, 'name':res['name'], 'state':res['state'], 'tag':tag}, context = None)
            return True


         # todo créer les arrow idem à cidessus res['start'} et res['stop'] en utilisant arrowdate.replace(heure) et
        # il faut utiliser la methode arw.replace(heure=8, minute=30) si start_h est de la forme 09:30 il saut start_h.lstrip("0")
        # puis un split(':')
        else:
                return {}

    _columns = {
                'name':fields.char('Name', size = 8, help = "Name for the open slots to be created"),
                'date':fields.date('Date', help = 'Day for slot to create'),
                "start_dt" : fields.datetime("Start", help = "First appointment  datetime"),
                "stop_dt": fields.datetime("Stop", help = "Last appointement  datetime"),
                "step" : fields.integer("Duration", help = "Duration of the slot (minutes)"),
                "ampm": fields.selection((("morning", _("Morning")), ("afternoon", _("Afternoon")), ("daylong", _("All day"))), "Day"),
                "start_h":fields.char('Start', size = 16, help = "Starting hour, eg: 08:00. Or starting of breakfast time for All day"),
                "end_h":fields.char('Stop', size = 16, help = "End period. eg: 12:00. This will be the end of the last slot, not the last slot. Or end of brakfast time for the All day"),
                "day_on":fields.char('Day On', size = 16, help = "Start of the day"),
                "day_off":fields.char('Day Off', size = 16, help = "End of the day"),
                "state": fields.selection(_get_status_agenda, 'State', readonly = False),
                            }
    _defaults = {
                 'step': 15,
                 'name': 'Factory',
                 'ampm':'daylong',
                 'day_on':'08:00',
                 'day_off':'16:30',
                 'state':'cs',
                }

agenda_factory()
# create(cr, user, vals, context=None)
# write(cr, user, ids, vals, context=None)¶

# Factory par 1/2 journée ou journée  TODO
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

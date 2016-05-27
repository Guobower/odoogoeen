# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import arrow
import inspect
import numpy as np
import pytz
import time
import rt5100 as rt

class oph_motive(orm.Model):
    """Motives for a crm.meeting"""
    _name = 'oph.motive'

    _columns = {
              'name':fields.char('Name', size = 32,),
              'comment':fields.text('Comment'),
              }
    _sql_constraints = [
                      ('name_uniq', 'unique(name)', 'The motive must be unique.'),
                      ]

class crm_meeting(orm.Model):
    _inherit = "crm.meeting"
    _description = "consultations meetings"
    _order = "date asc"

    def get_rt5100(self,cr,uid,ids,context=None):
        """Get the datas from the RT-5100
        """
        print 'IN GET_RT5100'
        print 'context:{}'.format(context)
        print "check I can import methods from rt5100"
        print 'SCADict:{}'.format(rt.SCAdict)
        
        finalDict = rt.getandformat_values()
        finalDict = rt.mergeandsubstitute(rt.map2odoofields(finalDict))
        print "final dict is :  {}".format(finalDict)
        
        for va_type in finalDict.keys():
            records=self.browse(cr,uid,ids,context)
            for record in records:
                print 'record.name:{}'.format(record.name)
                print 'record.partner_id:{}'.format(record.partner_id)
                print 'record.meeting_id:{}'.format(record.id)
                val_measurement={'va_type':va_type,
                                              'type_id':2,
                                              'meeting_id':record.id,
                                              }
                for k,v in finalDict[va_type].items():
                    val_measurement.update({k:v})
                #===============================================================
                # vals_measurement = {
                #             #'type_id.code' : 'ref', #TODO
                #             'type_id' : 2, # always the same. Is for refraction.
                #             'meeting_id' : record.id, #TODO
                #             'sph_od' : finalDict[va_type]['sph_od'],
                #             'cyl_od': finalDict[va_type]['cyl_od'],
                #             'axis_od':finalDict[va_type]['axis_od'],
                #             'sph_os' : finalDict[va_type]['sph_os'],
                #             'cyl_os':finalDict[va_type]['cyl_os'],
                #             'axis_os':finalDict[va_type]['axis_os'],
                #             'va_type':va_type
                #             }
                #===============================================================
                print 'vals : {}'.format(val_measurement)
                oph_measurement_obj =  self.pool.get('oph.measurement').create(cr, uid, val_measurement, context = context)
        return True
    

    def selection_partner_id(self, cr, uid, ids, context = None):
        """
        Get the partner_id from the res.partner to write it in the crm.meeting record
        """
        res = {}
        fmt = 'YYYY-MM-DD HH:mm:ss'
        print "PASSING IN: %s CONTEXT IS: %s" % (inspect.stack()[0][3], context)
        self.write(cr, uid, ids, {'partner_id':context.get('default_partner_id'), 'given_date':arrow.now().to('UTC').format(fmt), 'user_id':uid}, context = None)
        # set state to busy
        self.statechange_busy(cr, uid, ids, context)
        return res

    def default_get(self, cr, uid, fields, context = None):
        """ Surcharge la valeur par defaut de la durée d'un RDV"""
        res = super(crm_meeting, self).default_get(cr, uid, fields, context = context)
        res['duration'] = 0.25
        return res

    def onchange_slot(self, cr, uid, ids, state, date, duration, organizer, context = None):
        """
        This method to check and avoid creating slot when it's not desirable
        We start by searching the closed slot.
        """
        if context == None:
            context = {}
        # slot_ids = self.search(cr, uid, [('state', 'in', (('close',)))])# récupere tous les records close OK
        res = {'value': {}}
        print "PASSING through", inspect.stack()[0][3]
        print "STATE, DATE, DURATION, ORGANIZER: %s, %s, %s, %s" % (state, date, duration, organizer)
        slot_ids = self.search(cr, uid, [('date', '=', date)])
        print "RESULT OF SEARCH:", slot_ids
        for record in self.browse(cr, uid, slot_ids, context = context):
            print "RECORD DATE IS;", record.date
            print "DATE_DEADLINE IS", record.date_deadline
            print "PARTNER NAME:", record.partner_id.name
        if slot_ids:
           warning = {
         'title': _("Warning for a close slot"),
         'message': _("Well are you sure you want to add a slot"),
         }
           return {'value': res.get('value', {}), 'warning':warning}
        return {'value': {}}

    def onchange_partner_id(self, cr, uid, ids, state, given_date, context = None):
        """
        Set state to busy when partner_id not empty
        Set given_date is date when the appointement is given
        Set user_id to the user who give the appointment
        """
        print "PASSING IN: %s CONTEXT IS: %s" % (inspect.stack()[0][3], context)
        foo = self.read(cr, uid, ids, fields = ['write_date', ], context = context, load = '_classic_read')
        fmt = 'YYYY-MM-DD HH:mm:ss'
        return {'value':{'state':'busy', 'given_date':arrow.now().to('UTC').format(fmt), 'user_id':uid}}

    def onchange_dates(self, cr, uid, ids, start_date, duration = False, end_date = False, allday = False, context = None):
       res = super(crm_meeting, self).onchange_dates(cr, uid, ids, start_date, duration = duration, end_date = end_date, allday = allday, context = context)
       slot_ids = self.search(cr, uid, [('date', '=', start_date)])
       if slot_ids:
           res.update({'warning': {
                                'title': _("Warning for a close slot"),
                                'message': _("Well are you sure you want to add a slot"),
                     }})
       return res

    #===========================================================================
    # def _get_status_agenda(self, cursor, user_id, context = None):
    #     return (
    #             ('draft', _('Draft')),
    #             ('cs', _('Consultation')),
    #             ('tech', _('Technique')),
    #             ('open', _('Open')),
    #             ('busy', _('Busy')),
    #             ('close', _('Close')),
    #             ('cancel', _('Cancel')),
    #             ('no_show', _('No Show')),
    #             ('wait', _('Wait')),
    #             ('nwnm', _('No Wait')),
    #             ('in', _('In')),
    #             ('in_between', _('In Between')),
    #             ('done', 'Out'),
    #             ('office', _('Office')),  # pourquoi devoir rajouter cette valeur
    #             )
    #===========================================================================

    def statechange_draft(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "draft"}, context = context)
        return True
    def statechange_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "open"}, context = context)
        return True
    def statechange_close(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "close"}, context = context)
        return True
    def statechange_cancel(self, cr, uid, ids, context = None):
        """
        Set the state of crm.meeting record to cancel
        and create a new crm.meeting lot
        with the cancel crm.meeting
        """
        self.write(cr, uid, ids, {"state": "cancel"}, context = context)
        vals = self.read(cr, uid, ids, fields = ['date', 'duration', 'date_deadline', 'tag' ], context = context, load = '_classic_read')
        # vals est une liste de dictionnaire avec les données des records
       # from pdb import set_trace;set_trace()
        for record in vals:  # on boucle sur les données des record retournées.
        # record est un dictionnaire
        # comment récupérer le statut cs ou technique? C'est tag
        # pour info duration est de type float.
        # il nous faut supprimer la clef "id" qui est systématiquement fournie dans le return de read
            del record['id']
            # del context['default_partner_id']
            record.update({'name':'Ouvert', 'state':record['tag'], 'partner_id':False})
            self.create(cr, uid, record, context = context)
        return True

    def statechange_in(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "in"}, context = context)
        return True
    def statechange_in_between(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "in_between"}, context = context)
        return True
    def statechange_out(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        # set meeting to close
        self.write(cr, uid, ids, {"state": "done"}, context = context)
        # return True #uncomment if just want the change state to out
        # get info for the quotation
        meeting = self.browse(cr, uid, ids[0], context = context)  # comment if you don't want to open a quotation view
       # pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
        res = {'default_partner_id': meeting.partner_id.id,
               'default_pricelist_id': meeting.partner_id.property_product_pricelist.id,
               'default_date_acte':meeting.datewotime,
               'default_origin':'Office',
               }

        return {  # Comment if you don't want to open a quotation view
            'name': _('Bla bla'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            # 'context': "{'default_partner_id': %s}" % (meeting.partner_id.id,),
            # 'context': "{'default_partner_id': %s, 'default_date_acte':%s}" % (meeting.partner_id.id, meeting.datewotime),
            'context':res,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def statechange_free(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "done", "free":True}, context = context)
        return True

    def statechange_no_show(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "no_show"}, context = context)
        return True

    def statechange_busy(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "busy"}, context = context)
        return True

    def statechange_wait(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "wait"}, context = context)
        return True

    def statechange_nwnm(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "nwnm"}, context = context)
        return True

    def _get_datewotime(self, cr, uid, ids, field_name, arg, context = {}):
        """
        will get the date without timestamp from date
        giving possibility to search by date 
        """
        res = {}
        if context is None:
            context = {}
        fmt = '%Y-%m-%d %H:%M:%S'  # set format. Adapted to the format of stored dates in postgresql
        local_tz = pytz.timezone(context.get('tz', 'Pacific/Noumea'))  # get tz from context
        records = self.browse(cr, uid, ids, context)
        for record in records:
            wd = datetime.strptime(record.date, fmt,)  # convert string date from database to datetime py object
            wd = pytz.UTC.localize(wd)  # make aware datetime object needed for astimezone()
            wd = wd.astimezone(local_tz)  # convert UTC time to local time
            res[record.id] = wd.date()
            # print "In _GET_DATEWOTIME. res is: %s" % res
        return res

    def _format_fullmotive(self, cr, uid, ids, name, args, context = None):
        """
        Concatenate the motive and motive comment 
        to get the fullmotive
        So you can keep some statistics on motive
        and get real information for patient motive
        """
        res = {}
        for br in self.browse(cr, uid, ids, context = None):
            motive = br.motive.name or ''
            motivecomment = br.motive_comment or ''
            fullmotive = motive + ' ' + motivecomment
            res[br.id] = fullmotive
        return res

    _columns = {
                'subject':fields.char('Subject', size = 128, help = "Object of the meeting",),  # not sure it's usefull
                'motive':fields.many2one('oph.motive', 'Motive',),
                'motive_comment':fields.char('Comment', size = 128, help = 'Comment to precise the motive'),
                'fullmotive':fields.function(_format_fullmotive, type = 'char', size = 128, string = 'Full Motive', store = True, method = True),
                'chief_complaint':fields.text('Chief Complaint'),
                'state': fields.selection([
                                                    ('draft', _('Draft')),
                                                    ('cs', _('Consultation')),
                                                    ('tech', _('Technique')),
                                                    ('open', _('Open')),
                                                    ('busy', _('Busy')),
                                                    ('close', _('Close')),
                                                    ('cancel', _('Cancel')),
                                                    ('no_show', _('No Show')),
                                                    ('wait', _('Wait')),
                                                    ('nwnm', _('No Wait')),
                                                    ('in', _('In')),
                                                    ('in_between', _('In Between')),
                                                    ('done', 'Out'),
                                                    ('office', _('Office'))], readonly = False),
                'partner_id':fields.many2one('res.partner', 'Partner',),
                'tono_ids':fields.one2many('oph.measurement', 'meeting_id', 'Tonometry', domain = [('type_id.code', '=', 'tono')]),
                'refraction_ids':fields.one2many('oph.measurement', 'meeting_id', 'Refraction', domain = [('type_id.code', '=', 'ref')]),
                'keratometry_ids':fields.one2many('oph.measurement', 'meeting_id', 'Keratometry', domain = [('type_id.code', '=', 'ker')]),
                'va_ids':fields.one2many('oph.measurement', 'meeting_id', 'Visual Acuity', domain = [('type_id.code', '=', 'va')]),
                'sle_ids':fields.one2many('oph.measurement', 'meeting_id', 'Slit Lamp Exam', domain = [('type_id.code', '=', 'sle')]),
                'pachy_ids':fields.one2many('oph.measurement', 'meeting_id', 'Center Corneal Thickness', domain = [('type_id.code', '=', 'pachy')]),
                'datewotime':fields.function(_get_datewotime, method = True, type = 'date', string = 'DateWOtime', store = True),
                'todo_list_ids':fields.one2many('oph.todolist', 'meeting_id', 'TODO',),
                #===============================================================
                'medication_line_ids':fields.one2many('oph.medication.line', 'meeting_id', 'Medication Line'),
                # cut/paste to inherit class crm.meeting cf oph_prescription.py
                #===============================================================
                'reporting_line_ids':fields.one2many('oph.reporting', 'meeting_id', 'Reporting Line'),
                'conclusion_ids':fields.one2many('oph.measurement', 'meeting_id', 'Conclusion Line', domain = [('type_id.code', '=', 'conc')]),
                'miscellaneous_ids':fields.one2many('oph.measurement', 'meeting_id', 'Miscellaneous informations', domain = [('type_id.code', '=', 'misc')]),
                'tag':fields.selection([
                                        ('office', _('Office')),
                                        ('or', _('OR')),
                                        ('cs', _('Consultation')),  # Add for persistence usefull for change to cancel
                                        ('tech', _('Technique')),  # Add for persistence usefull for change to cancel
                                        ], 'Tag', select = True, readonly = True),
                'free':fields.boolean('Free', help = 'True if not invoiced'),  # for free consultation
                'neuro':fields.text('Neuro Observation'),
                'mh':fields.text('Medical History'),
                #'allergia':fields.one2many('oph.allergen', 'meeting_id', 'Allergia'),
                'pricelist':fields.related('partner_id', 'property_product_pricelist', type = 'many2one', relation = 'product.pricelist', string = 'Pricelist', store = False),
                'given_date':fields.datetime('Given Date', help = 'Date when the appointement is given to the partner'),
                }

    _defaults = {
                 'state': 'open',  # TODO is it OK
                 'name': 'RDV',
                 'duration' : 0.25,
                 'tag':'cs',
                 'free':False }

    def unlink(self, cr, uid, ids, context = None):
        for meeting in self.browse(cr, uid, ids, context = context):
            if meeting.state not in ('draft', 'open'):
                raise osv.except_osv(_('Error!'), _('Impossible to delete a meeting not in draft state  or open!'))
        return super(crm_meeting, self).unlink(cr, uid, ids, context = context)

class oph_measurement(orm.Model):
    _inherit = "oph.measurement"
    _columns = {
                'chief_complaint':fields.related('meeting_id', 'chief_complaint', type = 'char', string = 'Chief Complaint',),
                'motive':fields.related('meeting_id', 'motive', type = 'many2one', relation = 'oph.motive', store = True, string = "Motive"),
                }
# '
             # 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

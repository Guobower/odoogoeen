# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import arrow
import time
from datetime import datetime, timedelta, date  # A tester voir si c'est OK.
from mx import DateTime
import numpy as np
import pytz
import inspect

class oph_indication(orm.Model):
    """
    use for OR indications selection
    """
    _name = 'oph.indication'
    _order = 'name asc'

    _columns = {
              'name':fields.char('Name', size=128),
              'ivt':fields.boolean('IVT', help="Tick the box if it's an indication for IVT"),
              'comment':fields.text('Comment'),
                 }

class oph_gauge(orm.Model):
    """
    Vitreteotome Hand Piece Gauge
    """
    _name = "oph.gauge"

    _columns = {
              'name':fields.char('Name', size=64),
                 }

class oph_iol_type(orm.Model):
    """
    Informations on IOL
    Object where you define all informations on IOL's
    """
    _name = "oph.iol.type"
    _columns = {
                'name':fields.char("Model", size=64,),
                'code':fields.char('Code', size=16),
                'manufactor':fields.char('Manufactor', size=64,),
                'constant':fields.float('Constant Lens', digits=(16, 2),),
                'comment':fields.text('Comment',),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'iol_type_id', 'Lines',)
                }

class oph_anesthesia_type(orm.Model):
    """
    Anesthesia type
    Object where you define all informations on anesthesia
    """
    _name = 'oph.anesthesia.type'
    _columns = {
                'name':fields.char('Name', size=64,),
                'code':fields.char('Code', size=8,),
                'comment':fields.char('Comment', size=128),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'anesthesia_type_id', 'Lines',)
                }

class oph_procedure_type(orm.Model):
    """
    Surgery Procedure type and description
    """
    _name = 'oph.procedure.type'

    def _get_yesorno(self, cursor, user_id, context=None):
        return (
                ('yes', _('YES')),
                ('no', _('NO')),
                )

    _columns = {
                'name':fields.char('Name', size=128, translate=True),
                'shortname':fields.char('Short Name', size=64, translate=True),
                'code':fields.char('Code', size=64,),
                'dilatation':fields.selection([('yes', _('YES')), ('no', _('NO')), ], 'Dilatation',),
                'iol_status':fields.boolean('IOL Status', Help='For an IOL during this type of procedure thick the boxe',),
                'duration':fields.integer('Duration', help='Expected duration of procedure in minutes'),
                'comment':fields.char('Comment', size=128, help='Where you put all the stuff you need for the intervention'),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'procedure_type_id', 'Lines',),
                }

class oph_inpatient_type(orm.Model):
    """
    Inpatient type
    """
    _name = 'oph.inpatient.type'
    _columns = {
                'name':fields.char('Name', size=128,),
                'code':fields.char('Code', size=64,),
                'comment':fields.char('Comment', size=128),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'inpatient_type_id', 'Lines',),
                }

class oph_bloc_agenda(osv.osv):
    """
    TODO
    """
    _name = "oph.bloc.agenda"
    _rec_name = 'wd'
    #===========================================================================
    # def name_search(self, cr, uid, name, args = None, operator = 'ilike', context = None, limit = 100):
    #     """
    #     Add the possibility to search the agenda line by partner name
    #     """
    #     print "JE PASSE PAR NAME_SEARCH d'AGENDA LINE? CONTEXT is:", context
    #     print "To be fix"
    #     return False
    #===========================================================================

    def _get_wdandmonth2(self, cr, uid, ids, field_name, arg, context={}):
        """
        will get the week day in text (eg: friday, saturday,...)
        and month 'eg: junuary, february,....)
        Using datetime module
        """
        import pudb;pudb.set_trace()
        res = {}
        if context is None:
            context = {}
        fmt = '%Y-%m-%d %H:%M:%S'  # set format. Adapted to the format of stored dates in postgresql
        local_tz = pytz.timezone(context.get('tz', 'Pacific/Noumea'))  # get tz from context
        records = self.browse(cr, uid, ids, context)
        for record in records:
            wd = datetime.strptime(record.start_date, fmt,)  # convert string date from database to datetime py object
            wd = pytz.UTC.localize(wd)  # make aware datetime object needed for astimezone()
            wd = wd.astimezone(local_tz)  # convert UTC time to local time
            res[record.id] = wd.strftime("%A") + ' ' + wd.strftime("%d") + ' ' + wd.strftime("%B")
        print "PASSING in : %s. Type of wd is :%s" % (inspect.stack()[0][3], type(res))
        return res

    def _get_wdandmonth(self, cr, uid, ids, field_name, arg, context={}):
        """
        To humanize the date format
        Using the arrow python module.
        Get the date convert it to arrow and format it to readable human.
        """
        print "CONTEXT:%s" % (context,)
        res = {}
        if context is None:
            context = {}
        fmt = 'dddd D MMMM YYYY'  # to format the date: monday 1 junuary 3021
        records = self.browse(cr, uid, ids, context)
        for record in records:
            if record.name:
                wd = record.name
                wd = arrow.get(wd, 'YYYY-MM-DD').to('utc').format(fmt, locale=context['lang'])
                res[record.id] = wd
        return res
    #===========================================================================
    # def name_get(self, cr, uid, ids, context = None):
    #     if not ids:
    #         return []
    #     result = []
    #     for bloc in self.browse(cr, uid, ids, context = context):
    #         result.append((bloc.id, bloc.wd or ''))
    #     return result
    #  remplacé par _rec_name='wd'
    #===========================================================================

    _columns = {
                'name':fields.date('Date'),
                'partner_id':fields.many2one('res.partner', 'Owner', help='This is the owner of the agenda', domain=[('colleague', '=', True)]),  # We just need colleague here
                'start_date':fields.datetime('StartDate',),
                'end_date':fields.datetime('EndDate',),
                'comment':fields.text('Informations',),
                'wd':fields.function(_get_wdandmonth, method=True, type='char', string='Weekday', store=False),
                'active':fields.boolean('Active', help='if the active field is set to False, it will allow you to hide the bloc agenda without removing it.'),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'bloc_agenda_id', 'Lines',)}

    _defaults = {'active': 1, }

    _order = "name asc"
oph_bloc_agenda()


class oph_bloc_agenda_line(osv.osv):
    """
    TODO
    """
    _name = "oph.bloc.agenda.line"
    _order = "sequence"

    def _get_date(self, cr, uid, field_name, arg, context={}):
        """
        To get the date and use it for order and sort
        """
        res = {}
        if context is None:
            context = {}
        records = self.browse(cr, uid, ids, context)
        import pudb;pudb.set_trace()

    def _get_wdandmonth(self, cr, uid, ids, field_name, arg, context={}):
        """
        To humanize the date format
        Using the arrow python module.
        Get the date value of oph.
        """
        res = {}
        if context is None:
            context = {}
        fmt = 'dddd D MMMM YYYY'  # to format the date: monday 1 junuary 3021
        records = self.browse(cr, uid, ids, context)
        for record in records:
            if record.name:
                wd = record.name
                wd = arrow.get(wd, 'YYYY-MM-DD').to('utc').format(fmt, locale=context['lang'])
                print 'WD is :%s' % (wd,)
                res[record.id] = wd
        return res

    #===========================================================================
    # sous forme de fonction
    # cela n'est pas pris en compte pour la traduction.
    # en tout cas je n'ai pas réussi
    # def _ods_get(self, cr, uid, context = None):
    #     return [
    #             ('OD', _('Right Eye')),
    #             ('OS', _('Left Eye')),
    #             ]
    #===========================================================================
    def name_get(self, cr, uid, ids, context=None):
        """
        Returns the preferred display value (text representation) 
        for the records with the given ids. 
        By default this will be the value of the "name" column, 
        unless the model implements a custom behavior.
        
        @Return: type:list(tuple)
        @Returns: list of pairs (id,text_repr) for all records with the given ids.
        """
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            if record.bloc_agenda_id.wd:
                name = record.bloc_agenda_id.wd
            if record.partner_id.fullname:
                name += ' -' + record.partner_id.fullname
        # from pdb import set_trace;set_trace()
#             if record.firstname:
#                 name += ', ' + record.firstname
#             if record.dob:
#                 name += ', (' + str(record.dob) + ')'
#             if record.parent_id:
#                 name = "%s (%s)" % (name, record.parent_id.name)
#             if context.get('show_address'):
#                 name = name + "\n" + self._display_address(cr, uid, record, without_company = True, context = context)
#                 name = name.replace('\n\n', '\n')
#                 name = name.replace('\n\n', '\n')
#             if context.get('show_email') and record.email:
#                 name = "%s <%s>" % (name, record.email)
#             if record.age:
#                 name += ' / (' + str(record.age) + ')'
#             if record.gender:
#                 name += '(' + record.gender + ')'
            res.append((record.id, name))
        return res

    def _get_ane_type(self, cursor, user_id, context=None):
        return (
                ('ST', _('Sub-Tenon')),
                ('PERI', _('Peribulbar')),
                ('TOP', _('Topique')),
                )

    def _get_hospit_type(self, cursor, user_id, context=None):
        return (
                ('AMBU', 'Ambulatoire'),
                ('1NUIT', '1 Nuit hospit'),
                ('EXT', 'Externe'),
                )

    #===========================================================================
    # def _get_status_bloc_agenda_line(self, cursor, user_id, context = None):
    #     return (
    #             ('draft', _('Draft')),
    #             ('open', _('Open')),
    #             ('confirm', _('Confirm')),
    #             ('cancel', _('Cancel')),
    #             ('close', _('Close')),
    #             ('no_show', _('No Show')),
    #             )
    #===========================================================================

    def statechange_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"state": "draft"}, context=context)
        return True

    def statechange_open(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"state": "open"}, context=context)
        return True

    def statechange_confirm(self, cr, uid, ids, context=None):
        # from pdb import set_trace;set_trace()
        self.write(cr, uid, ids, {"state": "confirm"}, context=context)
        return True

    def statechange_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"state": "cancel", "sequence":0}, context=context)
        return True

    def statechange_close(self, cr, uid, ids, context=None):
        """
        change state to close
        create a record in crm_meeting
        create a record in oph.todolist with tag_id is "Normal", name="CROP"
        create a record in oph.recording ready to print a report
        """
        self.write(cr, uid, ids, {"state": "close"}, context=context)
        print "ids:%s" % ids
        print "context:%s" % context
        if context is None:
            context = {}
        lines = self.browse(cr, uid, ids, context=context)

        # create a meeting for each bloc agenda line
        for l in lines:
            vals_meeting = {
                  'name':'OR',
                  'motive_comment':l.procedure_type_id.name + ' ' + l.ods.upper(),  # Doesn't work.
                  'partner_id':l.partner_id.id,
                  'datewotime':l.bloc_agenda_id.name,
                  'date':l.bloc_agenda_id.name,
                  'date_deadline':l.bloc_agenda_id.name,
                  'state':'done',
                  'tag':'or',
                  }
            crm_meeting_obj = self.pool.get('crm.meeting').create(cr, uid, vals_meeting, context=context)

            # create a oph.reporting to be ready to make the OR report
            vals_reporting = {
                        'name':l.procedure_type_id.name + ' ' + l.ods.upper() + ' (' + l.bloc_agenda_id.name + ')',
                        'meeting_id':crm_meeting_obj,
                        'ods':l.ods,
                        'type':'ORR',
                        'iol_type':l.iol_type_id.name,
                        'iol_power':l.iol_power,
                        'anesthesia_id':l.anesthesia_type_id.id,
                        'receiver_partner':True,
                        }
            print "VALS_REPORTING: %s" % vals_reporting
            reporting_obj = self.pool.get('oph.reporting').create(cr, uid, vals_reporting, context=context)
        # return True

        # Getting a quotation if bloc_agenda_line set to close
        agenda_line = self.browse(cr, uid, ids[0], context=context)
        res = {'default_partner_id':agenda_line.partner_id.id,
               'default_pricelist_id': agenda_line.partner_id.property_product_pricelist.id,
               'default_date_acte':agenda_line.bloc_agenda_id.name,
               'default_origin':'OR'
               }
        return {  # Comment if you don't want to open a quotation view
            'name': _('Set A Quotation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'context':res,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    def statechange_noshow(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"state": "no_show"}, context=context)
        return True

    def _get_ic_selection(self, cr, uid, context=None):
        """
        ic is for informed consent
        """
        return (
                ('draft', 'Draft'),
                ('open', 'Open'),
                ('close', 'Close'),
                )

    def ic_open(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"ic": "open"}, context=context)
        return True

    def ic_close(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {"ic": "close"}, context=context)
        return True

    def onchange_set_duration(self, cr, uid, ids, procedure_type_id, dilatation, context=None):
        obj_procedure_type = self.pool.get('oph.procedure.type').browse(cr, uid, procedure_type_id, context=None)
        print "ONCHANGE DURATION"
        if obj_procedure_type.dilatation == 'yes':
            dilatation = True
        else:
            dilatation = False
        val = {'value':{'duration':obj_procedure_type.duration, 'dilatation':dilatation}}
        print "VAL:%s" % (val,)
        return val

    _columns = {
                'name':fields.char('Id', size=8,),
                'date':fields.function(_get_date, method=True, type='date', string='Date', store=True),
                'wd':fields.function(_get_wdandmonth, method=True, type='char', string='Weekday', store=False),
                'sequence':fields.integer('Sequence'),
                'duration':fields.float('Duration',),
                'start_time':fields.char('Horaire', size=8),
                'partner_id':fields.many2one('res.partner', 'Partner', required=True),
                'state': fields.selection([('draft', _('Draft')),
                                                    ('open', _('Open')),
                                                    ('confirm', _('Confirm')),
                                                    ('cancel', _('Cancel')),
                                                    ('close', _('Close')),
                                                    ('no_show', _('No Show')), ], 'State', readonly=False),
                'comment':fields.text('Comment'),
                'ods':fields.selection([('OD', _('Right Eye')),
                                         ('OS', _('Left Eye')), ], 'ODS', required=True,),
                'snd_eye':fields.boolean('Second Eye'),
                # 'ane_type':fields.selection(_get_ane_type, 'ANE', required = True,),
                'anesthesia_type_id':fields.many2one('oph.anesthesia.type', 'Anesthesia Type'),
                'dilatation':fields.boolean('Dilatation', help="Tick the box if the patient must be dilated"),
                'inpatient_type_id':fields.many2one('oph.inpatient.type', 'Inpatient Type',),
                'iol_type_id':fields.many2one('oph.iol.type', 'IOL Type'),
                'iol_power':fields.float('IOL Power', digits=(4, 2)),
                'bloc_agenda_id':fields.many2one('oph.bloc.agenda', 'Bloc Agenda',),
                'procedure_type_id':fields.many2one('oph.procedure.type', 'Procedure Type', required=True),
                # 'duration_procedure':fields.related('procedure_type_id', 'duration', type = 'integer', string = 'Duration Procedure'),
                'gauge_id':fields.many2one('oph.gauge', 'Gauge', help='Vitrectomy gauge'),
                # 'duration_procedure':fields.integer('Duration', 'Estimated procedure duration in minutes'), # Moins bien que le duration fields.float car pas de calcul du total en bas de la colonne
                'procedure_iol_status':fields.related('procedure_type_id', 'iol_status', type='boolean', string='IOL Procedure',),
                'ic':fields.selection(_get_ic_selection, 'Informed Consent', help='Check if informed consent has been delivered to and given back by the patient'),
                'ane_appointment':fields.datetime('Date ANE RDV', help='date appointment for anesthesia'),
                'ane_comment':fields.char('comment ANE', char='128'),
                'po_meeting_id':fields.many2one('crm.meeting', 'PostOR Appointment'),
                'indication_id':fields.many2one('oph.indication', 'Indication'),
                # 'operator_id':fields.many2one('res.users', 'Operator'),
                'operator_id':fields.many2one('res.partner', 'Operator'),
                'notification_time':fields.char('Notification Time', size=8),
                'cim10_id':fields.many2one('oph.cim10', string="CIM10 codification", help="CIM 10 codification",),
                'bloc_agenda_line_id':fields.many2one('oph.bloc.agenda.line', string="OR", help="ref an other OR",),
                }

    _defaults = {
                 'state': 'draft',
                 'ic': 'draft',
                 'dilatation':True,  # will be set in onchange_set
                 'operator_id':lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).partner_id.id
                 }

oph_bloc_agenda_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

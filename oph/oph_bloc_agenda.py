# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime, timedelta, date  # A tester voir si c'est OK.
from mx import DateTime
import numpy as np
import pytz

class oph_iol_type(osv.osv):
    """
    Informations on IOL
    Object where you define all informations on IOL's
    """
    _name = "oph.iol.type"
    _columns = {
                'name':fields.char("Model", size = 64,),
                'code':fields.char('Code', size = 16),
                'manufactor':fields.char('Manufactor', size = 64,),
                'constant':fields.float('Constant Lens', digits = (16, 2),),
                'comment':fields.text('Comment',),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'iol_type_id', 'Lines',)
                }
oph_iol_type()

class oph_anesthesia_type(osv.osv):
    """
    Anesthesia type
    Object where you define all informations on anesthesia
    """
    _name = 'oph.anesthesia.type'
    _columns = {
                'name':fields.char('Name', size = 64,),
                'code':fields.char('Code', size = 8,),
                'comment':fields.char('Comment', size = 128),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'anesthesia_type_id', 'Lines',)
                }
oph_anesthesia_type()

class oph_procedure_type(osv.osv):
    """
    Surgery Procedure type and description
    """
    _name = 'oph.procedure.type'

    def _get_yesorno(self, cursor, user_id, context = None):
        return (
                ('yes', _('YES')),
                ('no', _('NO')),
                )

    _columns = {
                'name':fields.char('Name', size = 128, translate = True),
                'code':fields.char('Code', size = 64,),
                'dilatation':fields.selection(_get_yesorno, 'Dilatation',),
                'iol_status':fields.boolean('IOL Status', Help = 'For an IOL during this type of procedure thick the boxe',),
                'duration':fields.integer('Duration', help = 'Expected duration of procedure in minutes'),
                'comment':fields.char('Comment', size = 128, help = 'Where you put all the stuff you need for the intervention'),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'procedure_type_id', 'Lines',)
                }
oph_procedure_type()

class oph_inpatient_type(osv.osv):
    """
    Inpatient type
    """
    _name = 'oph.inpatient.type'
    _columns = {
                'name':fields.char('Name', size = 128,),
                'code':fields.char('Code', size = 64,),
                'comment':fields.char('Comment', size = 128),
                'line_ids':fields.one2many('oph.bloc.agenda.line', 'inpatient_type_id', 'Lines',),
                }
oph_inpatient_type()

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

    def _get_wdandmonth(self, cr, uid, ids, field_name, arg, context = {}):
        """
        will get the week day in text (eg: friday, saturday,...)
        and month 'eg: junuary, february,....)
        """
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
                'partner_id':fields.many2one('res.partner', 'Owner', help = 'This is the owner of the agenda', domain = [('colleague', '=', True)]),  # We just need colleague here
                'start_date':fields.datetime('StartDate',),
                'end_date':fields.datetime('EndDate',),
                'comment':fields.text('Informations',),
                'wd':fields.function(_get_wdandmonth, method = True, type = 'char', string = 'Weekday',),
                'active':fields.boolean('Active', help = 'if the active field is set to False, it will allow you to hide the bloc agenda without removing it.'),
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

    def _get_wdandmonth(self, cr, uid, ids, field_name, arg, context = {}):
        """
        will get the week day in text (eg: friday, saturday,...)
        and month 'eg: junuary, february,....)
        All datetime are in UTC in the database. So we have to convert them in local time 
        before getting day string an month string. If not you will get the  day and month
        of date in UTC.
        We use pytz for that. And we get information of timezone with context.
        But if there is no context or info on tz in context 
        we set tz = 'Pacific/Noumea'. Maybe this is not what you want in your place.
        """
        res = {}
        if context is None:
            context = {}
        fmt = '%Y-%m-%d %H:%M:%S'  # set format. Adapted to the format of stored dates in postgresql
        local_tz = pytz.timezone(context.get('tz', 'Pacific/Noumea'))  # get tz from context
        records = self.browse(cr, uid, ids, context)
        for record in records:
            wd = datetime.strptime(record.bloc_agenda_id.start_date, fmt,)  # convert string date from database to datetime py object
            wd = pytz.UTC.localize(wd)  # make aware datetime object. Needed for astimezone()
            wd = wd.astimezone(local_tz)  # convert UTC datetime to local datetime
            res[record.id] = wd.strftime("%A") + ' ' + wd.strftime("%d") + ' ' + wd.strftime("%B")
        return res

    def _ods_get(self, cr, uid, context = None):
        return [
                ('OD', _('Right Eye')),
                ('OS', _('Left Eye')),
                ]

    def _get_ane_type(self, cursor, user_id, context = None):
        return (
                ('ST', _('Sub-Tenon')),
                ('PERI', _('Peribulbar')),
                ('TOP', _('Topique')),
                )

    def _get_hospit_type(self, cursor, user_id, context = None):
        return (
                ('AMBU', 'Ambulatoire'),
                ('1NUIT', '1 Nuit hospit'),
                ('EXT', 'Externe'),
                )

    def _get_status_bloc_agenda_line(self, cursor, user_id, context = None):
        return (
                ('draft', _('Draft')),
                ('open', _('Open')),
                ('confirm', _('Confirm')),
                ('cancel', _('Cancel')),
                ('close', _('Close')),
                ('no_show', _('No Show')),
                )

    def statechange_draft(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "draft"}, context = context)
        return True

    def statechange_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "open"}, context = context)
        return True

    def statechange_confirm(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "confirm"}, context = context)
        return True

    def statechange_cancel(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "cancel"}, context = context)
        return True

    def statechange_close(self, cr, uid, ids, context = None):
        """
        change state to close
        create a record in crm_meeting
        create a record in oph.todolist with tag_id is "Normal", name="CROP"
        create a record in oph.recording ready to print a report
        """
        self.write(cr, uid, ids, {"state": "close"}, context = context)
        print "ids:%s" % ids
        print "context:%s" % context
        if context is None:
            context = {}
        lines = self.browse(cr, uid, ids, context = context)

        # create a meeting for each bloc agenda line
        for l in lines:
            vals_meeting = {
                  'name':'OR',
                  'motive_comment':l.procedure_type_id.name + ' ' + l.ods.upper(),  # Doesn't work.
                  'partner_id':l.partner_id.id,
                  'datewotime':l.bloc_agenda_id.name,
                  'date':l.bloc_agenda_id.name,
                  'date_deadline':l.bloc_agenda_id.name,
                  'state':'out',
                  'tag':'or',
                  }
            crm_meeting_obj = self.pool.get('crm.meeting').create(cr, uid, vals_meeting, context = context)

            # create a oph.reporting to be ready to make the OR report
            vals_reporting = {
                        'name':l.procedure_type_id.name + ' ' + l.ods.upper() + ' (' + l.bloc_agenda_id.name + ')',
                        'meeting_id':crm_meeting_obj,
                        'ods':l.ods,
                        'type':'ORR',
                        'iol_type':l.iol_type_id.name,
                        'iol_power':l.iol_power,
                        'anesthesia_id':l.anesthesia_type_id.id,
                        }
            reporting_obj = self.pool.get('oph.reporting').create(cr, uid, vals_reporting, context = context)
        # return True

        # Getting a quotation if bloc_agenda_line set to close
        agenda_line = self.browse(cr, uid, ids[0], context = context)
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

    def statechange_noshow(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "no_show"}, context = context)
        return True

    def _get_ic_selection(self, cr, uid, context = None):
        """
        ic is for informed consent
        """
        return (
                ('draft', 'Draft'),
                ('open', 'Open'),
                ('close', 'Close'),
                )

    def ic_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"ic": "open"}, context = context)
        return True

    def ic_close(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"ic": "close"}, context = context)
        return True

    def onchange_set_duration(self, cr, uid, ids, procedure_type_id, dilatation, context = None):
        obj_procedure_type = self.pool.get('oph.procedure.type').browse(cr, uid, procedure_type_id, context = None)
        print "ONCHANGE DURATION"
        if obj_procedure_type.dilatation == 'yes':
            dilatation = True
        else:
            dilatation = False
        val = {'value':{'duration':obj_procedure_type.duration, 'dilatation':dilatation}}
        print "VAL:%s" % (val,)
        return val

    _columns = {
                'name':fields.char('Id', size = 8,),
                'wd':fields.function(_get_wdandmonth, method = True, type = 'char', string = 'Weekday',),
                'sequence':fields.integer('Sequence'),
                'duration':fields.float('Duration',),
                'start_time':fields.char('Horaire', size = 8),
                'partner_id':fields.many2one('res.partner', 'Partner', required = True),
                'state': fields.selection(_get_status_bloc_agenda_line, 'State', readonly = False),
                'comment':fields.text('Comment'),
                'ods':fields.selection(_ods_get, 'ODS', required = True,),
                'snd_eye':fields.boolean('Second Eye'),
                # 'ane_type':fields.selection(_get_ane_type, 'ANE', required = True,),
                'anesthesia_type_id':fields.many2one('oph.anesthesia.type', 'Anesthesia Type'),
                'dilatation':fields.boolean('Dilatation', help = "Tick the box if the patient must be dilated"),
                'inpatient_type_id':fields.many2one('oph.inpatient.type', 'Inpatient Type',),
                'iol_type_id':fields.many2one('oph.iol.type', 'IOL Type'),
                'iol_power':fields.float('IOL Power', digits = (4, 2)),
                'bloc_agenda_id':fields.many2one('oph.bloc.agenda', 'Bloc Agenda',),
                'procedure_type_id':fields.many2one('oph.procedure.type', 'Procedure Type', required = True),
                # 'duration_procedure':fields.related('procedure_type_id', 'duration', type = 'integer', string = 'Duration Procedure'),
                'gauge_id':fields.many2one('oph.gauge', 'Gauge', help = 'Vitrectomy gauge'),
                # 'duration_procedure':fields.integer('Duration', 'Estimated procedure duration in minutes'), # Moins bien que le duration fields.float car pas de calcul du total en bas de la colonne
                'procedure_iol_status':fields.related('procedure_type_id', 'iol_status', type = 'boolean', string = 'IOL Procedure',),
                'ic':fields.selection(_get_ic_selection, 'Informed Consent', help = 'Check if informed consent has been delivered to and given back by the patient'),
                'ane_appointment':fields.date('Date ANE RDV', help = 'date appointment for anesthesia'),
                'ane_comment':fields.char('comment ANE', char = '128'),
                'po_meeting_id':fields.many2one('crm.meeting', 'PostOR Appointment'),
                'indication_id':fields.many2one('oph.indication', 'Indication'),
                'operator_id':fields.many2one('res.users', 'Operator'),
                }

    _defaults = {
                 'state': 'draft',
                 'ic': 'draft',
                 'dilatation':True,  # will be set in onchange_set
                 'operator_id':lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).partner_id.id
                 }

oph_bloc_agenda_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

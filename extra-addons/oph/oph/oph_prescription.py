# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
from datetime import datetime

class exam(orm.Model):
    """
    Table for exams
    """
    _name = 'oph.exam'

    def _get_sel(self, cursor, user_id, context = None):
        return (
                ('Bio',_('Biology')),
                ('Rx', _('Radiology')),
                ('Cx', _('Cardiology')),
                )

    _columns = {
              'type_id':fields.selection(_get_sel, 'Type', size = 8),
              'name':fields.char('Name', size = 64),
              'code':fields.char('Code', size = 16),
              'comment':fields.text('Comment'),
              }

class oph_brandname(orm.Model):
    """
    Table of the brand name med
    """
    _name = 'oph.brandname'

    def onchange_name(self, cr, uid, id, name, context = None):
        if context == None:
            context = {}
        return {'value':{'name':(name.upper() if name else '')}}

    _columns = {
             'name':fields.char('Name', size = 64, help = 'brand name'),
             'brandname_id':fields.many2one('oph.inn', 'INN'),
             'galenique':fields.char('Galenique', char = 64, help = 'galenique'),
             'line_ids':fields.one2many('oph_medication_line', 'brandname_id', 'Lines'),
             'ivt':fields.boolean('For IVT', help = 'To be injected in vitreous'),
             'ods_needed':fields.boolean('ODS Needed', help = 'Need to specify ODS in prescription'),
             }

class oph_inn(orm.Model):
    """
    Table of the International Nonproprietary Names
    DCI dénomination Commune internationale
    """
    _name = 'oph.inn'

    def onchange_name(self, cr, uid, id, name, context = None):
        if context == None:
            context = {}
        return {'value':{'name':(name.lower() if name else '')}}

    _columns = {
              'name':fields.char('Name', size = 128, help = 'INN'),
              'alternate':fields.char('Alernate', size = 32, help = 'INN'),
              'comment':fields.text('Comment'),
              'brandname_ids':fields.one2many('oph.brandname', 'brandname_id', 'BrandName'),
              'ivt':fields.boolean('IVT', help = 'Used for intravitreal injection'),
              }

class oph_medication_line(orm.Model):
    """
    TODO
    """

    _name = 'oph.medication.line'

    def _get_ods(self, cursor, user_id, context = None):
        return (
                ('od', _('Right Eye')),
                ('os', _('Left Eye')),
                ('ods', _('Right and Left Eye'))
                )

    _columns = {
                'name':fields.char('Id', size = 8),
                'meeting_id':fields.many2one('crm.meeting', 'CRM MEETING'),
                'brandname_id':fields.many2one('oph.brandname', 'BRANDNAME'),
                'poso':fields.char('POSO', size = 64),
                'duration':fields.char('Duration', size = 64),
                'ods':fields.selection(_get_ods, 'ODS', required = False,),
                'comment':fields.text('Comment'),
                'date':fields.related('meeting_id', 'date', type = 'date', string = 'Consultation Date', store = True),
                'partner_id':fields.related("meeting_id", "partner_id", type = "many2one", relation = "res.partner", string = "Partner", store = True, readonly = True,),
                'ods_needed':fields.related('brandname_id', 'ods_needed', type = 'boolean', store = True, string = "ods_needed"),
              }


class pathology(orm.Model):
    """
    In pathology ods fields is unusefull
    """
    _name = 'oph.pathology'

    def _get_ods(self, cursor, user_id, context = None):
        return (
                ('od', _('Right Eye')),
                ('os', _('Left Eye')),
                ('ods', _('Right and Left Eye'))
                )

    _columns = {
              'name':fields.char('Name', size = 32),
              'medication_line_ids':fields.one2many('oph.medication.line.template', 'pathology_id', 'Lines'),
              'comment':fields.text('Comment', help = 'Used to add some informations on the prescription report'),
              'ods':fields.selection(_get_ods, 'ODS', required = False,),
              }

class oph_medication_line_template(orm.Model):
    """
    Table with the medication linked to a pathology
    the field ods is not usefull
    """
    _name = 'oph.medication.line.template'

    def _get_ods(self, cursor, user_id, context = None):
        return (
                ('od', _('Right Eye')),
                ('os', _('Left Eye')),
                ('ods', _('Right and Left Eye'))
                )

    _columns = {
                'name':fields.char('Id', size = 8),
                'brandname_id':fields.many2one('oph.brandname', 'BRANDNAME'),
                'poso':fields.char('POSO', size = 64),
                'duration':fields.char('Duration', size = 64),
                'ods':fields.selection(_get_ods, 'ODS', required = False,),  # Pas utile dans le template car sera a definir au niveau crm.meeting
                'comment':fields.text('Comment'),
                'pathology_id': fields.many2one('oph.pathology', 'Pathology', required = False),  # True pose problem
              }

class oph_protocole(orm.Model):
    _name = 'oph.protocole'
    _columns = {
              'name':fields.char('Name', size = 32),
              'comment':fields.text('Comment'),
              'protocole_line_ids':fields.one2many('oph.protocole.line.template', 'protocole_id', 'Lines'),
              'comment':fields.text('Comment'),
              }

class oph_protocole_line_template(orm.Model):
    """
    TODO
    """

    _name = 'oph.protocole.line.template'

    def _get_ods(self, cursor, user_id, context = None):
        return (
                ('od', _('Right Eye')),
                ('os', _('Left Eye')),
                ('ods', _('Right and Left Eye'))
                )

    _columns = {
                'name':fields.char('Id', size = 8),
                'exam_id':fields.many2one('oph.exam', 'Exam'),
                'ods':fields.selection(_get_ods, 'ODG', required = False,),  # Pas utile dans le template car sera a definir au niveau crm.meeting
                'comment':fields.text('Comment'),
                'protocole_id': fields.many2one('oph.protocole', 'Protocole', required = False),  # True pose problem
              }
class oph_protocole_line(orm.Model):
    """
    TODO
    """
    _name = 'oph.protocole.line'

    def _get_ods(self, cursor, user_id, context = None):
        return (
                ('od', _('Right Eye')),
                ('os', _('Left Eye')),
                ('ods', _('Right and Left Eye'))
                )

    _columns = {
                'name':fields.char('Id', size = 8),
                'meeting_id':fields.many2one('crm.meeting', 'CRM MEETING'),
                'ods':fields.selection(_get_ods, 'ODS', required = False,),
                'comment':fields.text('Comment'),
                'date':fields.related('meeting_id', 'date', type = 'date', string = 'Consultation Date', store = True),
                'exam_id':fields.many2one('oph.exam', 'Exam'),
                'result':fields.text('Result', help = "Exam result"),
                'partner_id':fields.related("meeting_id", "partner_id", type = "many2one", relation = "res.partner", string = "Partner", store = True, readonly = True,),
              }



class crm_meeting(orm.Model):
    _inherit = 'crm.meeting'

    def create_defaults_medication_lines(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        line_obj = self.pool.get('oph.medication.line')
        for meeting in self.browse(cr, uid, ids, context = context):
            for pathology in meeting.pathology_ids:
                for line in pathology.medication_line_ids:
                    line_obj.create(cr, uid, {
                            'meeting_id': meeting.id,
                            'name': line.name,
                            'brandname_id': line.brandname_id.id,
                            'ods': line.ods,
                            'poso': line.poso,
                            'duration': line.duration,
                            'comment': line.comment,
                    }, context = context)
        return True

    def create_defaults_protocole_lines(self, cr, uid, ids, context = None):
        if context is None:
            context = {}
        line_obj = self.pool.get('oph.protocole.line')
        for meeting in self.browse(cr, uid, ids, context = context):
            for protocole in meeting.protocole_ids:
                for line in protocole.protocole_line_ids:
                    line_obj.create(cr, uid, {
                                            'meeting_id':meeting.id,
                                            'name':line.name,
                                            'exam_id':line.exam_id.id,
                                            'ods':line.ods,
                                            'result':False,
                                            'comment':line.comment,
                                            }, context = context)
        return True

    _columns = {
              'medication_line_ids':fields.one2many('oph.medication.line', 'meeting_id', 'Medication Line'),
              'pathology_ids':fields.many2many('oph.pathology', 'oph_pathology_meeting_rel', 'meeting_id', 'pathology_id', 'Pathology Line'),
              'protocole_ids':fields.many2many('oph.protocole', 'oph_protocole_meeting_rel', 'meeting_id', 'protocole_id', 'Protocole Line'),
              'protocole_line_ids':fields.one2many('oph.protocole.line', 'meeting_id', 'Protocole Line'), }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

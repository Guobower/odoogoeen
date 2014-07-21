# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
from datetime import datetime
import inspect
import arrow

class oph_indication(orm.Model):
    """
    use for OR indications selection
    """
    _name = "oph.indication"

    _columns = {
              'name':fields.char('Name', size = 128),
              'ivt':fields.boolean('IVT', help = "Tick the box if it's an indication for IVT"),
                 }

class oph_gauge(orm.Model):
    """
    Vitreteotome Hand Piece Gauge
    """
    _name = "oph.gauge"

    _columns = {
              'name':fields.char('Name', size = 64),
                 }

class oph_lens(orm.Model):
    """
    Table for lens usualy for laser treatment or biomicroscopy.
    Not use for biomicroscopy in the application
    """
    _name = "oph.lens"

    _columns = {
              'name':fields.char('Name', size = 64),
              'model':fields.char('Model', size = 64),
              'magnification':fields.float('Magnification'),
                 }

class oph_reporting(orm.Model):
    _name = 'oph.reporting'

    def _type_get(self, cr, uid, context = None):
        return [
                ('Off', _('Office Report')),
                ('Laser', _('Laser Report')),
                ('FAF', _('Fluoresceine Angiography Report')),
                ('OCT', _('OCT Report')),
                ('ORR', _('Operating Room Report')),
                ('DIAB', _('Diabetic')),
                ('IVT', _('IntraVitreal Injection')),
                 ]

    def on_change_receiver(self, cr, uid, ids, receiver_id, context = None):
        print 'IN ON_CHANGE_RECEIVER'
        if context is None:
            context = {}
        values = {}

        obj = self.pool.get('oph.honorific')
        res = obj.search(cr, uid, [('user_id', '=', uid), ('partner_id', '=', receiver_id)], context = context)

        if not res:  # si search ne trouve rien alors il retourne une liste vide []
            values = {'honorific':True}
            return {'value':values}

        res = obj.read(cr, uid, res, fields = ['honorific'], context = context)
        values = {'honorific':res[0].get('honorific')}  # provisoire pour les tests
        return {'value':values}

    def _state_get(self, cr, uid, context = None):
        return [
                    ('draft', 'Draft'),
                    ('open', 'Open'),
                    ('close', 'Close'),
                    ]

    def statechange_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "open"}, context = context)
        return True

    def statechange_close(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "close"}, context = context)
        return True

    def __ods_get(self, cr, uid, context = None):
        return (
                ('OD', _('Right Eye')),
                ('OS', _('Left Eye')),
                ('ODS', _('Right and Left Eye'))
                )
#===============================================================================
#
#     def create(self, cr, uid, vals, context = None):
#         from pdb import set_trace
#         set_trace()
#         return super(oph_reporting, self).create(cr, uid, vals, context)
#===============================================================================

    def _get_default_name(self, cr, uid, context = None):
        """
        Return a string 
        "Report-Patient Name-date of the day"
        Comment je fais pour récupérer le partner_id.fullname 
        """
        if context == None:
            context = {}
        obj_meeting = self.pool.get('crm.meeting')
        name = obj_meeting.browse(cr, uid, context['active_id'], context = context).partner_id.fullname

        # import pdb;pdb.set_trace()
        date = arrow.now().to(context['tz']).format("DD-MM-YYYY")
        return "Report_" + name + '_' + date

    def _get_next_meeting(self, cr, uid, context = None):
        """
        Return a string
        Return month is in french not very convinient for internationalisation..
        """
        nummonth = range(12)
        strmonth = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
        mappedmonth = dict(zip(nummonth, strmonth))

        ny = arrow.now()
        if ny.day >= 15:
            ny = ny.replace(months = +13)
        else:
            ny = ny.replace(months = +12)
        ny = mappedmonth[ny.month] + ' ' + str(ny.year)
        print "PASSING IN:%s. CONTEXT:%s" % (inspect.stack()[0][3], context)
        print "RETURN: %s" % (ny,)
        return ny
    
    def get_default_body_text(self, cr, uid, id, context = None):
        """
        Will get the body text from the template_id record
        """
        if context is None:
            context={}
        template_obj = self.pool.get('oph.reporting.template')
        for report in self.browse(cr, uid, id, context = context):
            template_rec = template_obj.read(cr, uid, report.template_id.id, ['text_body', ], context = context)
            self.write(cr, uid, report.id, {'text_body':template_rec.get('text_body', '')}, context = context)
        return True
            
    _columns = {
              'name':fields.char('Name', size = 128, help = "Name report"),
              'type':fields.selection(_type_get, 'Type'),
              'meeting_id':fields.many2one('crm.meeting', 'Meeting', select = True),
              'partner_id':fields.related("meeting_id", "partner_id", type = "many2one", relation = "res.partner", string = "Partner", store = True, readonly = True,),
              'date':fields.related('meeting_id', 'date', type = 'date', string = 'Consultation Date', store = True),
              'header_id':fields.many2one('oph.reporting.template', string = 'Header', domain = [('type', '=', 'H')], help = "Header for OR report"),
              'vitreotome_machine':fields.text('Vitreotome mention'),
              'tech_op_phako':fields.text('Tech op phako', help = 'Tech op phako information'),
              'template_id':fields.many2one('oph.reporting.template', 'Reporting Template', select = True),
              'text_body':fields.text('Text Body', help = 'Text body of the report'),
              # many2one ou many2many?
              # je penche plutot pour many2many et pourquoi je pense qu'il ne peut y avoir qu'un seul template
              'template_ids':fields.many2many('oph.reporting.template', 'oph_reporting_reporting_template_rel', 'reporting_id', 'reporting_template_id', 'Reporting Templates', domain = [('active', '=', True)]),
              # coordonnées du destinataire pour remplir l'entete automatiquement
              'receiver_id':fields.many2one('res.partner', 'Receiver', domain = [('colleague', '=', True)]),
              'receiver_partner':fields.boolean('Receiver Patient', help = "Patient is the receiver"),
              'cc_partner':fields.boolean('Copie Patient', help = "Thick the box, if sending a copie to the patient"),
              'dictate_wpatient':fields.boolean('Dictate with patient', help = "Thick the box, if dictate with patient"),
              'cc_ids':fields.many2many('res.partner', 'reporting_partner_rel', 'reporting_id', 'partner_id', 'Copies', domain = [('colleague', '=', True)]),
              # a qui j'écris au patient lui meme dans ce cas là c'est direct par partner_id
              #
              # faire un champ "adressé par" dans le crm_meeting à remplir par la secrétaire.
              # mention copie à / remis en main / LR/AR propre.à imprimer dnas le dossier aussi
              # le probleme c'est que dans ces templates je ne peux pas mettre des champs dynamiques.
              # l'avantage c'est que les modeles sont rangés dans une database et des vues
              # sinon ils ont rangés dans des boutons.
              'lens':fields.many2one('oph.lens', 'Lens'),
              'laser_power':fields.integer('Laser Power'),
              'impact_size':fields.integer('Impact Size'),
              'impact_number':fields.integer('Impacts number'),
              'HbA1c':fields.float('HbA1c'),
              'next_meeting':fields.char('Next Year', size = 32),
              'quand':fields.char('When', size = 16),
              'iol_power':fields.float('IOL power', digits = (4, 2)),
              'iol_type':fields.char('IOL Type', size = 16),
              'var1':fields.char('US Total Time', size = 16),
              'var2':fields.float('PT', help = "Puissance Totale equivalente en position 3"),
              'var3':fields.float('EDC', help = "Energie dissipée cumulée"),
              'var4':fields.char('TT', size = 16, help = "Temps de Torsion"),
              'var5':fields.float('Amp T M', help = "Amplitude de Torsion Moyenne"),
              'var6':fields.float('Amp T M P3', help = "Amplitude de Torsion Moyenne en position 3"),
              'var7':fields.float('Amp T M Eq P3', help = "Amplitude de Torsion Moyenne equivalente en position 3"),
              'bv':fields.boolean('Blue Vision', help = 'Use of Blue Vision'),
              'sutureless':fields.boolean('Sutureless'),
              'air_bubble':fields.boolean('Air Bubble'),
              'gauge_id':fields.many2one('oph.gauge', 'Gauge', help = 'Vitrectomie gauge'),
              # 'molecule':fields.selection(_molecule_get, 'Molecule', help = "Intravitreal Injected molecule(s)"),
              # I want to have more than one molecule
              'molecule_ids':fields.many2many('oph.inn', 'oph_reporting_inn_rel', 'reporting_id', 'inn_id', 'Molecule(s)'),  # marche pas domain = [('ivt', 'is', True)],
              'indication_id':fields.many2one('oph.indication', 'Indication'),
              'ods':fields.selection(__ods_get, 'ODS', required = False,),
              'state':fields.selection(_state_get, 'State'),
              # text_body:fields.text qui serait construit par concaténation des text_body des templates et insertions des données var1....
              'honorific':fields.boolean('Honorific'),
              'anesthesia_id':fields.many2one('oph.anesthesia.type', 'Anesthesia'),
              'post_op_treatement':fields.text('Post Operatoire Treatement'),
              'positionnement':fields.text('Positionnement'),
              'retinal_thickness_od':fields.integer('Retinal Thickness OD'),
              'retinal_thickness_os':fields.integer('Retinal Thickness OS'),
              }

    _defaults = {
               'state':'draft',
               'name':_get_default_name,
               'vitreotome_machine':'Constellation Alcon. Mise en service novembre 2011',
               'tech_op_phako':'Technique Ozyl. Sonde Kellman 30° 0.9mm. Microincision',
               'next_meeting':_get_next_meeting,
                    }

class oph_reporting_template(orm.Model):
    _name = 'oph.reporting.template'

    def _type_get(self, cr, uid, context = None):
        return [('Off', _('Office Report')),
                ('ORR', _('Operating Room Report')),
                ('DIAB', _('Diabetic')),
                ('IVT', _('IntraVitreal Injection')),
                ('H', _('Header')),
                ('His', _('History')),
                ('Ex', _('Exam')),
                ('ASS', _('Anterior Segment Section')),
                ('PSS', _('Posterior Segment Section')),
                ('CS', _('Conclusion Section')),
                ('Laser', _('Laser Report')),
                ('FAF', _('Fluoresceine Angiography Report')),
                ('OCT', _('OCT Report')),
                ]

    _columns = {
              'name':fields.char('Name', size = 128, help = "Name of the template"),
              'short_name':fields.char('Short Name', size = 64),
              'text_body':fields.text('Text Body', help='Text body of the template'),
              'type':fields.selection(_type_get, 'Type'),
              'active':fields.boolean('Active', help = "If False the template wont be selectable"),
              }

    _defaults = {
               'active':True,
               }

class oph_request(orm.Model):
    _name = 'oph.request'

    def on_change_oph_partner(self, cr, uid, ids, partner_id, date_request, context = None):
        if context is None:
            context = {}
        values = {}
        res_partner = self.pool.get('res.partner')
        # import pdb;pdb.set_trace()
        br = res_partner.browse(cr, uid, partner_id, context = None)
        name = 'Demande Accord' + ' ' + br.fullname + ' ' + date_request

        return {'value': {'name': name}}

    def request_open(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "open"}, context = context)
        return True

    def request_close(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "close"}, context = context)
        return True

    def request_cancel(self, cr, uid, ids, context = None):
        self.write(cr, uid, ids, {"state": "cancel"}, context = context)
        return True

    def _state_get(self, cr, uid, context = None):
        return [
                    ('draft', 'Draft'),
                    ('open', 'Open'),
                    ('close', 'Close'),
                    ('cancel', 'Cancelled'),
                    ]

    def _priority_id_selection(self, cr, uid, context = None):
        tag_id_obj = self.pool.get('oph.todolist.tag')
        # tag_ids = tag_id_obj.search(cr, uid, [('default', '=', True), ], context = context)
        tag_ids = tag_id_obj.search(cr, uid, [], context = context)
        if tag_ids:
            res = tag_id_obj.read(cr, uid, tag_ids, ['name'], context = context)
            return [(str(r['id']), r['name']) for r in res]
        return True

    _columns = {
                'name':fields.char('Name', size = 128),
                'comment':fields.char('Comment', size = 128),
                'partner_id': fields.many2one('res.partner', 'Partner', change_default = True, required = True,),
                'referent_id':fields.many2one('res.partner', 'Referent', domain = [('colleague', '=', True)], required = True,),
                'request_line_ids':fields.one2many('oph.request.line', 'request_id', 'Accord Lines'),
                'date_request': fields.date('Request Date', readonly = True, states = {'draft':[('readonly', False)]}, select = True, help = "Keep empty to use the current date"),
                'state':fields.selection(_state_get, 'Status', select = True, readonly = True),
                'company_id': fields.many2one('res.company', 'Company', required = True, change_default = True, readonly = True, states = {'draft':[('readonly', False)]}),
                'priority_id':fields.selection(_priority_id_selection, 'Priority'),
                }

    _defaults = {
        'state': 'draft',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context = c),
        'date_request': lambda *a: time.strftime('%Y-%m-%d'),
                }

class oph_request_line(orm.Model):
    _name = 'oph.request.line'


    _columns = {
                'name':fields.char('Name', size = 16),
                'sequence': fields.integer('Sequence', help = "Gives the sequence of this line when displaying the invoice."),
                'request_id':fields.many2one('oph.request', 'Accord Reference', ondelete = "cascade", select = True),
                'product_id':fields.many2one('product.product', 'Product', select = True),
                'partner_id':fields.related('request_id', 'partner_id', type = 'many2one', relation = 'res.partner', string = 'Partner', store = True),
                'comment':fields.char('Comment', size = 128),
                }



class res_partner(orm.Model):
    """ Inherits partner and adds invoice information in the partner form """
    _inherit = 'res.partner'
    _columns = {
                'request_ids': fields.one2many('oph.request.line', 'partner_id', 'Accords CAFAT', readonly = True),

                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

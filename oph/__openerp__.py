# -*- coding: utf-8 -*-

# fichier lu qd on install le module
# avec administration/module/import module.
#
{
    'name' : 'Ophthalmology',
    'version' : '0.1',
    'author' : 'Cabinet GOEEN',
    'category': 'Generic Modules/Others',
    'description': """
Module de consultation pour l'ophtalmologiste
=======================================================================================

Permet de faire pleins de choses absolument géniales
                """,
    'website': '',
    'depends' : [
                 "base",
                 "account",
                 "account_voucher",
                 "account_accountant",
                 "account_cancel",
                 "crm",
                 "base_calendar",
                 "report_aeroo",
                 "report_aeroo_ooo",
                 "l10n_fr",
                 "sale",
                 "knowledge",
                 "document",
                 "document_ftp",
                 "portal",
                 ],
    'data': [
        'security/oph_security.xml',
        'security/ir.model.access.csv',

#        'custom/oph_custom_view.xml',

#        'custom/oph_meeting_view.xml',
#        'oph_agenda_workflow.xml',
        'wizard/oph_agenda_factory_view.xml',
        'wizard/oph_etat_factory_view.xml',
        'report/Test_premier_report.xml',
        'oph_bloc_agenda_view.xml',
        'report/examination_report.xml',
        'report/bloc_agenda_report.xml',
        'data/ir.config_parameter.xml',
        'data/measurement_type.xml',
        'data/oph_iol_type_data.xml',
        'data/inpatient_type_data.xml',
        'data/procedure_type_data.xml',
        'data/anesthesia_type_data.xml',
        'data/product_data.xml',
        # 'data/document_data.xml',
        'oph_measurement_view.xml',
        'oph_instrumentation_view.xml',
        'oph_reporting_view.xml',
        'oph_agenda_view.xml',
        'custom/oph_partner_view.xml',
        'custom/oph_phonecall_view.xml',
        'custom/oph_invoice_view.xml',
        'custom/oph_sale_view.xml',
        'oph_prescription_view.xml',
        'oph_filling_template.xml',
        'data/filling_template_data.xml',
        'data/prescription_data.xml',
        'data/reporting_template_data.xml',
        'wizard/oph_formula_prescription_view.xml',
        'wizard/oph_diabetic_report_view.xml',
        'custom/oph_res_users_view.xml',
        'custom/account_voucher_view.xml',
        'wizard/oph_ivt_prescription_view.xml',
        'wizard/oph_crm_meeting_state_view.xml',
        'wizard/oph_account_voucher_deposit_view.xml',
        ],
    'demo': [
                 'demo/oph_partner_demo.xml',
                 'demo/bloc_agenda_demo.xml',
                 'demo/oph_agenda_demo.xml',
                 ],
    'test': [],
    'installable': True,
    'active': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

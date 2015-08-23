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
                'custom/oph_partner_view.xml',
                'custom/oph_res_users_view.xml',
                'custom/oph_sale_order_view.xml',
                'custom/oph_account_invoice_view.xml',
                'custom/oph_account_voucher_view.xml',
                'custom/oph_crm_phonecall_view.xml',
                'custom/oph_phonecall_view.xml',
                # 'custom/oph_invoice_view.xml',
                'oph_prescription_view.xml',
                'oph_instrumentation_view.xml',
                'oph_measurement_view.xml',
                'oph_agenda_view.xml',
                'data/measurement_type.xml',
                'data/prescription_data.xml',
                'data/procedure_type_data.xml',
                'data/filling_template_data.xml',
                'oph_bloc_agenda_view.xml',
                'report/stylesheet/stt_report.xml',
                'report/bloc_agenda_report.xml',
                'oph_filling_template.xml',
                'oph_reporting_view.xml',
                'report/oph_reporting_report.xml',
                'report/crm_meeting_report.xml',
                'report/sale_order_report.xml',
                'report/account_invoice_report.xml',
                'wizard/oph_agenda_factory_view.xml',
                'wizard/oph_formula_prescription_view.xml',
                'wizard/oph_ivt_prescription_view.xml',
                'wizard/oph_account_voucher_deposit_view.xml',
                'wizard/oph_crm_meeting_state_view.xml',
                'wizard/oph_day_template_view.xml',
                # 'wizard/oph_day_template_agenda_factory_view.xml',
                'oph_prescription_view.xml',
                'data/surgery_data.xml',
                'data/product_data.xml',
                'data/anesthesia_type_data.xml',
                'data/inpatient_type_data.xml',
                'wizard/oph_etat_factory_view.xml',
                'oph_request_view.xml',
                'oph_config_surgery_view.xml',
                'data/oph_iol_type_data.xml',
                'data/reporting_template_data.xml',
                'report/examination_report.xml',
                'edi/request_action_data.xml',
       #========================================================================
       #  'report/Test_premier_report.xml',
       #
       #  'data/ir.config_parameter.xml',
       #  # 'data/document_data.xml',
# #
# #        'custom/oph_sale_view.xml',
#         # # 'data/reporting_template_data.xml',
#         # # 'wizard/oph_diabetic_report_view.xml',
#         #=======================================================================
        # 'custom/account_voucher_view.xml',
        #=======================================================================
        ],
    #===========================================================================
    # 'demo': [
    #              'demo/oph_partner_demo.xml',
    #              'demo/bloc_agenda_demo.xml',
    #              'demo/oph_agenda_demo.xml',
    #              ],
    #===========================================================================
    'test': [],
    'installable': True,
    'active': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

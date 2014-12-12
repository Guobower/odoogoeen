# -*- coding: utf-8 -*-
from openerp.osv import fields, osv, orm

class crm_phonecall(orm.Model):
    _inherit = "crm.phonecall"

    def action_make_meeting(self, cr, uid, ids, context = None):
        """
        Open meeting's calendar view to schedule a meeting on current phonecall.
        :return dict: dictionary value for created meeting view
        """
        phonecall = self.browse(cr, uid, ids[0], context)
        res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'base_calendar', 'action_crm_meeting', context)
        res['context'] = {
            'default_phonecall_id': phonecall.id,
            # 'default_partner_ids': phonecall.partner_id and [phonecall.partner_id.id] or False,
            'default_partner_id': phonecall.partner_id and phonecall.partner_id.id or False,
            'search_default_partner_id': False,
            'default_user_id': uid,
            'default_email_from': phonecall.email_from,
#            'default_state': 'open',
            'default_name': phonecall.name,
        }
        return res
    
    _columns = { 'comment':fields.text('Comment'),
                }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
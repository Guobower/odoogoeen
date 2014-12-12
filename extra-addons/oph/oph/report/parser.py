# -*- coding: utf-8 -*-
#############################################################################
#
# Copyright (c) 2008-2011 Alistek Ltd (http://www.alistek.com) All Rights Reserved.
#                    General contacts <info@alistek.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This module is GPLv3 or newer and incompatible
# with OpenERP SA "AGPL + Private Use License"!
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from report import report_sxw
from report.report_sxw import rml_parse
from lxml import etree
import pooler
from collections import Iterable
from datetime import datetime
import pytz
import locale
from openerp.tools import ustr
import arrow


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.context = context
        self.localcontext.update({
            'arrow_today_timestamp':self.arrow_today_timestamp,
            'arrow_today':self.arrow_today,
            'printed_date':self.printed_date,
            'date_report' : self._date_report,
            'hba1c':self._val_hba1c,
            'receiver':self._receiver,
            'subtotal':self.subtotal,
            'rebate':self.rebate,
            'total':self.total,
            'total_chq':self.total_chq,
            'only_time':self.get_only_time,
            # 'molecule':self._get_molecule,
            # 'indication':self._get_indication,
            # 'molecule1':self._get_molecule1,
            # 'ref_statement':self._ref_statement,
        })
    def arrow_today(self):
        fmt = 'DD-MM-YYYY'
        return arrow.now().format(fmt)

    def arrow_today_timestamp(self):
        fmt = 'DD-MM-YYYY HH:mm'
        return arrow.now().format(fmt)

    def printed_date(self):
        return datetime.now().strftime("%y-%m-%d")

    def _date_report(self, context = None):
        if context is None:
            context = {}
        context = self.context
        import pdb;pdb.set_trace()
        return context.get('date_report', '')

    def _ref_statement(self, context = None):
        if context is None:
            context = {}
        context = self.context
        return context.get('ref_statement', '')

    def _val_hba1c(self, context = None):
        if context is None:
            context = {}
        context = self.context
        return context.get('hba1c', "Je n'ai pas retrouve")

    def _receiver(self, context = None):
        if context is None:
            context = {}
        context = self.context
        return context.get('receiver')

    def subtotal(self, context = None):
        print "PASSING SUBTOTAL"
        if context is None:
            context = {}
        context = self.context
        res = {'subtotal':0}
        temp = self.pool.get(context.get('active_model')).browse(self.cr, self.uid, context.get('active_ids'))
        for invoice in temp:
            for line in invoice.invoice_line:
                res['subtotal'] += line.price_subtotal
        context['subtotal'] = res.get('subtotal')
        return context.get('subtotal')

    def total_chq(self, context = None):
        print "PASSING TOTAL"
        if context is None:
            context = {}
        context = self.context
        res = {'subtotal':0}
        temp = self.pool.get(context.get('active_model')).browse(self.cr, self.uid, context.get('active_ids'))
        for rec in temp:
            res['subtotal'] += rec.amount
        context['subtotal'] = res.get('subtotal')
        return context.get('subtotal')

    def rebate(self, context = None):
        context = self.context
        context['rebate'] = context.get('subtotal') * 0.1
        return context.get('rebate')

    def total(self, context = None):
        context = self.context
        context['total'] = context.get('subtotal') - context.get('rebate')
        return context.get('total')

    def get_only_time(self, context = None):
        if context is None:
            context = {}
        context = self.context
        temp = self.pool.get(context.get('active_model')).browse(self.cr, self.uid, context.get('active_ids'))
        for rec in temp:
            context['only_time'] = rec.date
        unaware = datetime.strptime(context['only_time'], '%Y-%m-%d %H:%M:%S')
        aware = unaware.replace(tzinfo = pytz.UTC)
        localized = aware.astimezone(pytz.timezone(context.get('tz')))
        # import pdb;pdb.set_trace()
        loc = locale.getlocale()
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # marche pas apres avoir fait un
        # dpkg-reconfigure locales
        # label = localized.strftime("%A %d %B %Y") + ' ' + u'à' + ' ' + localized.strftime("%H H %M")
        label = ustr(localized.strftime("%A %d %B %Y")) + ' ' + u'à' + ' ' + ustr(localized.strftime("%H H %M"))
        # print 'aware %s, LOCALIZED %s' % (aware, localized)
        # print 'date en anglais %s' % (localized.strftime("%A %d %B %Y"))
        # print 'heure %s' % (localized.strftime("%H H %M"))
        context['only_time'] = label

        print 'REC.DATE TYPE and VALUE: %s %s' % (type(rec.date), rec.date)
        return context.get('only_time', '')

    def _molecule(self, context = None):
        if context is None:
            context = {}
        context = self.context
        return context.get('molecule', '')

    def _indication(self, context = None):
        if context is None:
            context = {}
        context = self.context
        return context.get('indication', '')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# Dans les methodes dans context on a comme clef: active_model qui est le nom du model depuis lequel on a appele le wizard. On a la date du report
# on a les active_ids qui sont les ids (sous forme de list) des records de l'object qui est l'active model
# mais on ne peut pas fair un search car cr n'est pas dans les arguments.
# on doit pouvoir
# invoice_oj.browse(self.cr,self.uid,context.get('active_ids'))
# [browse_record(account.invoice, 2), browse_record(account.invoice, 1)]


# -*- coding: utf-8 -*-
# parser permettant de récupérer les données du popup etat_factory.py
from report import report_sxw
from lxml import etree
import pooler

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.context = context
        self.localcontext.update({
            'date_report' : self._date_report,
        })

    def _date_report(self, context=None):
        if context is None:
            context = {}
        context = self.context
        return context.get('date_report', '')

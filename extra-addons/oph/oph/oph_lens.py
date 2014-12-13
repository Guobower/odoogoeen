# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

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
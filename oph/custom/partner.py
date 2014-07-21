# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from mx import DateTime
from openerp.tools.translate import _
# ====================================================================
# dired:
# 01 12  2012
# Created by:   FRANCOIS Laurent
# filename:     partner.py
# Comment: Custom partner object for oph
# ===================================================================
# --
class res_partner(osv.osv):
    _inherit = "res.partner"

    def onchange_name(self, cr, uid, id, firstname, lastname, dob, context = None):
        """
        Will put fullname = LASTNAME, Firstname 
        in field name of table res.partner
        """
        if context == None:
            context = {}
        fullname = ''
        warning = False
        if dob:
            """
            Looking for an hononymus in database
            """
            partner_ids = self.search(cr, uid, [('dob', '=', dob), ('name', 'like', lastname), ('firstname', 'like', firstname)], limit = 1, context = context)
            if partner_ids:
                warning = {}
                warning['title'] = _('Caution')
                warning['message'] = _('There is already an homonyme with the same birthdate')
        # return {'value' : {'name': (lastname.upper() if lastname else ''), 'firstname': (firstname.capitalize() if firstname else '')}, 'warning': warning}
        return {'value': {'name':(lastname.upper() if lastname else ''), 'firstname':(' '.join(map(str, map(lambda w:w.capitalize(), firstname.split()))) if firstname else '')}, 'warning':warning}


    def _format_fullname(self, cr, uid, ids, name, args, context = None):
        """
        Will put fullname = LASTNAME, Firstname 
        in field name of table res.partner
        """
        res = {}
        for m in self.browse(cr, uid, ids, context = context):
            firstname = m.firstname
            lastname = m.name
            fullname = ''
            if lastname:
                # fullname=(lastname.upper() if lastname else '') + (", " +firstname.capitalize() if firstname else '')
                fullname = (lastname.upper() if lastname else '') + (", " + ' '.join(map(str, map(lambda w:w.capitalize(), firstname.split()))) if firstname else '')
            res[m.id] = fullname
        return res

    def _get_age(self, cr, uid, ids, field_name, arg, context = {}):
        # print 'JE PASSE PAR _GET_AGE et CONTEXT is:', context
        res = {}
        records = self.browse(cr, uid, ids, context)
        date = DateTime.today()
        for record in records :
            age = ''
            res[record.id] = {
                'age' : '',
            }
            birthdate = False
            if record.dob:
                birthdate = DateTime.strptime(record.dob, '%Y-%m-%d')
                year, month, day = birthdate.year, birthdate.month, birthdate.day
            if birthdate:
                day = int(day)
                month = int(month)
                year = int(year)
                if (date.month > month) or (date.month == month and date.day >= day):
                    if (date.year - year) >= 2:
                        age = str(date.year - year) + _(' YO')
                    else:
                        if date.year == year:
                            age = str(date.month - month) + _(' month')
                        else:
                            age = str(12 + date.month - month) + _(' month')
                else:
                    if (date.year - year - 1) >= 2:
                        age = str(date.year - year - 1) + _(' YO')
                    else:
                        months = date.month - month
                        if date.month == month:
                            months = -1
                        if date.year == year:
                            age = str(months) + _(' month')
                        elif date.year == year + 1:
                            age = str(12 + months) + _(' month')
                        elif date.year == year + 2:
                            age = str(24 + months) + _(' month')
            res[record.id]['age'] += age
        return res

    def _get_trusted(self, cr, uid, context = None):
        if context == None:
            context = {}
        return context.get('trusted', False)

    def _get_customer(self, cr, uid, context = None):
        """
        Cette methode retourne la bonne valeur je pense
        mais il y a autre chose qui surcharge le default customer
        a True
        """
        if context == None:
            context = {}
        res = True
        if context.get('trusted') or context.get('colleague'):
                res = False
        return res

    def _get_colleague(self, cr, uid, context = None):
        if context == None:
            context = {}
        return context.get('colleague', False)

    def _get_carte(self, cr, uid, context = None):
        return [
                    ('cafatmut', 'CAFAT MUT'),
                    ('b', 'AMG B SUD'),
                    ('bn', 'AMG B NORD'),
                    ('lm', 'LM'),
                    ]

    _columns = {
               'firstname': fields.char("Firstname", size = 64),
               # champ calculé/stocké pour LASTNAME,Firstname
               'fullname':fields.function(_format_fullname, type = 'char', size = 128, string = 'Fullname', store = True, method = True),
               'gender': fields.selection([('M', 'Male'), ('F', 'Female')], 'Gender',),
               'dob': fields.date('Date of Birth'),
               'age': fields.function(_get_age, method = True, type = 'char', string = 'Age', multi = 'all'),
               'cafatid': fields.char('CAFAT Number', size = 64),
               'carte':fields.selection(_get_carte, 'Carte'),
               'amgid': fields.char("N°AMG", size = 64),
               'PO_box':fields.char('PO box', size = 8),
               'partner_ids': fields.many2many('res.partner', 'res_partner_relation_rel', 'partner_id', 'related_id', 'Relations', domain = [('colleague', '=', True)]),
               # domain pour n'avoir que les colleagues dans l'onglet Relations.
               'colleague': fields.boolean('Colleague'),
               'trusted':fields.boolean('Trusted', help = 'Used for partner which are a trusted budy for an other patient'),
               'trusted_partner_ids': fields.many2many('res.partner', 'res_partner_trusted_rel', 'partner_id', 'trusted_id', 'Trusted Partner', domain = ['|', '|', ('customer', '=', True), ('trusted', '=', True), ('colleague', '=', True)]),
               'comment_secure':fields.text('Secured Comment', help = 'Comment not to be shared'),
               }

    _defaults = {
               'trusted':lambda s, cr, uid, c:s._get_trusted(cr, uid, context = c),
               'customer':lambda s, cr, uid, c:s._get_customer(cr, uid, context = c),
               'colleague':lambda s, cr, uid, c:s._get_colleague(cr, uid, context = c),
               }

    def name_get(self, cr, uid, ids, context = None):
        """
        Returns the preferred display value (text representation) 
        for the records with the given ids. 
        By default this will be the value of the "name" column, 
        unless the model implements a custom behavior.
        
        @Return: type:list(tuple)
        @Returns: list of pairs (id,text_repr) for all records with the given ids.
        """
        print "JE PASSE PAR NAME_GET "
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context = context):
            name = record.name
            if record.firstname:
                name += ', ' + record.firstname
            if record.dob:
                name += ', (' + str(record.dob) + ')'
            if record.parent_id:
                name = "%s (%s)" % (name, record.parent_id.name)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company = True, context = context)
                name = name.replace('\n\n', '\n')
                name = name.replace('\n\n', '\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            if record.age:
                name += ' / (' + str(record.age) + ')'
            res.append((record.id, name))
        return res

    def name_search(self, cr, uid, name, args = None, operator = 'ilike', context = None, limit = 100):
        print "JE PASSE PAR NAME_SEARCH et CONTExT is:", context
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            # search on the name of the contacts and of its company
            search_name = name
            # print "SEARCH_NAME is %s" % (name,)
            # print "CONTEXT IS:", context
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]
            if ' / ' in search_name:
                search_name = search_name.split(' / ')[0]
                search_name += "%"
            query_args = {'name': search_name}
            limit_str = ''
            if limit:
                limit_str = ' limit %(limit)s'
                query_args['limit'] = limit
            cr.execute('''SELECT partner.id 
                                FROM res_partner partner
                                LEFT JOIN res_partner company 
                                ON partner.parent_id = company.id
                               WHERE partner.email ''' + operator + ''' %(name)s
                               OR partner.fullname || ', (' || partner.dob || ')' || ' (' || COALESCE(company.name,'') || ')' ''' + operator + ' %(name)s '
                               ''' OR partner.fullname || ' (' || COALESCE(company.name,'') || ')' ''' + operator + ' %(name)s '
                               + limit_str, query_args)
            ids = map(lambda x: x[0], cr.fetchall())
            if args:
                ids = self.search(cr, uid, [('id', 'in', ids)] + args, limit = limit, context = context)
            if ids:
                return self.name_get(cr, uid, ids, context)
        return super(res_partner, self).name_search(cr, uid, name, args, operator = operator, context = context, limit = limit)



res_partner()


class oph_honorific(osv.osv):
    _name = 'oph.honorific'

    _columns = {
              'user_id':fields.many2one('res.users', 'User Id'),
              'honorific':fields.boolean('Honorific', help = 'Tick the box if vous'),
              'partner_id':fields.many2one('res.partner', 'Partner Id', domain = [('colleague', '=', True)], help = 'Partner'),
              }
    _defaults = {
               'honorific': True,
               'user_id': lambda obj, cr, uid, context = None: uid,  # comment mettre le user_id default
               }

oph_honorific()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

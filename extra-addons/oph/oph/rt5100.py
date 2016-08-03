# -*- coding: utf-8 -*-
"""
TODO
"""
import re, os
import logging

_logger = logging.getLogger(__name__)

# constants
SCAdict = {'f':('subjectdata', 'FarVisionSCA'),
           'n':('subjectdata', 'NearVisionSCA'),
           'F':('finalprescriptiondata', 'FarVisionSCA)'),
           'N':('finalprescriptiondata', 'NearVisionSCA'),
           'O':('ARdata', 'ObjectiveSCA'),
               }

cuttingSCA = [0, 2, 8, 14, 17]
cuttingADD = [0, 2, 8]
cuttingVA = [0, 2, 7]

# dict use by merge and substitute method.
# keys ('a','A','f','F','n','N') are the first character that code the line of the
# output file from rt5100

# RT datas after a line @RT before an other @:
# AR datas (autorefractometer datas)
#     O objective SCA
#     V corrected visual acuity
#     U corrected visual acuity extended format

# After à @RM before an other @
# Unaided visual acuity datas
#    W unaided visual acuity
#    M unaided visual acuity extended format

# Final prescription datas : F, N,  A, V
#     F: far vision SCA datas
#     N: near vision SCA datas
#     A: ADD
#     V: Visual acuity
#     U: visual acuity with extended format
#
# Subjective datas
#     f : far vision SCA
#     n : near vision SCA
#     a : ADD
#     v : visual acuity
#     u : visual acuity extended format

# for the left and right,  rt5100 append "L" or "R" to this letter.
# eg vL visual acuity for left eye.
# for binoculare rt5100 append the character "B":
# eg  UB for

mapvatype = {'a':'BCVA',
             'A':'Rx',
             'f':'BCVA',
             'F':'Rx',
             'n':'BCVA',
             'N': 'Rx',
              }
# not used
mappedvatype = {'BCVA':('a', 'f', 'n'),  # ceux sont les deux seuls valeurs qui ont besoins de SCA et ADD. Pour les verres portes ce n'est pas le RT5100 qui le donne.
                'Rx':('F', 'N', 'A')}  # Rx stand for prescription

#===============================================================================
# Pour l'instant dans ODOO je n'utilise pas  les valeurs de 'nN' qui est la formule SCA de pres (=avec l'ADD')
#===============================================================================

#===============================================================================
# cuttingDict={  'a':[28,30,36], # a if for add. 28 cut the timpstamp, 30 the data type and R or L, 36 the value= '+' 'dizaine unité' 'dot' 'decimal1' 'decimal2'
#                     'A':[28,30,36], # A for addition
#                     'f':[28, 30, 36, 42, 45],
#                     'F':[1,7,13,16],
#                     'O':[1,7,13,16],
#                     'n': [28, 30, 36, 42, 45],
#                     'N': [28, 30, 36, 42, 45],
#                     }
#===============================================================================

regexADD = r'[Aa][RL]'  # regex to get the line with ADD datas
regexSCA = r'[OfFnN][RL]'  # regex tp get the line with SCA datas.
regexVA = r'[VUWMvu][RLB]'  # regex to catch datas for VA


# map regex and the way to cut the line to get the datas
cuttingDict = { regexADD:cuttingADD,
                regexSCA:cuttingSCA,
                regexVA:cuttingVA,
                  }

def zero2none(val):
    """Set val to None if val is 0.00, + 0.00, - 0.00
    """
    rx = '[1-9]|[a-zA-Z]'
    if not re.search(rx, val, flags = 0):
        val = None
    return val

def trimzero(val):
    """Trim zero value if there is one at the 2nd decimal
    needed if there is a selection fields with no zero at the 2nd decimal
    in Odoo
    
    val : string from the rt5100
    
    example: '+ 2.20' return '+ 2.2'
    example: '100' return '100'
    """
    res = val
    regex = r'\.\d0'
    if re.search(regex, val, flags = 0):
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
        if val[-1] == '0':
            res = val[:-1]
    return res

def trimspace_regex(val):
    """Trim the space after sign +/- if there is one in val
    val : string from rt-5100
    eg val = '+ 2,00'  --> return '+2.00'
    eg val ='  0,00'   --> return '  0.00'

    return the trimed string
    """
    regex = r'^[+-] '  # don't forget the space at the end of the regex
    if re.search(regex, val, flags = 0):
        # match = re.search(regex, val, flags = 0)
        # print 'match:{}'.format(match)
        val = val[:1] + val[2:]
    return val

def trim_timestamp(line, lenght = 28):
    """Trim the timestamp
    
    because I don't need it and the timestamp is always the same lengh 
    exept if you change the code in the getting program from the rt5100
    
    line : str line from the data file
    lenght : int lenght of the timestamp
    
    return : str the line without the timestamp.
    """
    res = line[lenght:]
    return res

def cutting(line, coupures):
    """ Cut the line into a list fields of datas
    
    line : str from the datas file fetched from rt5100
    
    coupures: list with size for cutting. depends on description of datas
    
    return: list of fields of datas 
    eg return: values:['FR', '- 2.00', '  0.00', '  0']; ['AL', '+ 1.50']
    the item can't be used like that in odoo database they must be formated.
    You can use the return of this function in list comprehénsion to format the items
    """
    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])]  # on coupe les lignes en morceaux qui isolent les champs.
    values = morceaux[1:-1]  # on élimine le champ date et on récupere que les champs datas.SCA dans une liste
    # print 'values:{0} ; morceaux:{1}'.format(values,morceaux)
    return values


def getandformat_values(rxlist = [regexSCA, regexADD, regexVA], log_path = os.path.expanduser('~') + '/rt5100rs232/tmp.log'):
    """ Get the values and format them ready to write in odoo
    
    rxlist : list of regex from specification of datas RT5100
    log_path: str path to file with datas from rt5100
    
    return : list of datas
    eg: return [['FL', '+20.75', '-6.00'], ['FR', '+20.75', '-6.00']]
    Those datas could be inserted in the database except that you need to map them to field names.
    """
    res = []
    for line in reversed(open(log_path).readlines()):
        if line.find('NIDEK') == -1:  # il n'y a pas le motif Nidek
            _logger.info('brut line:%s', line)
            line = trim_timestamp(line)
            _logger.info('no timestamp line: %s', line)
            for rx in rxlist:
                if re.search(rx, line, flags = 0):
                    values = cutting(line, cuttingDict[rx])
                    _logger.info('cutting values: %s', values)
                    values = [val.strip() for val in values]
                    values = [trimspace_regex(val) for val in values]
                    _logger.info('formated trimspaced values: %s', values)
                    # values = [zero2none(val) for val in values]
                    _logger.info('val:%s', val)
                    _logger.info('type(val):%s', type(val))
                    if re.search(rxlist[0], line, flags = 0):  # don't trimzero ADD values.
                        values = [trimzero(val) for val in values]
                        _logger.info('trimzero: %s', values)
                    res.append(values)
#                    values=[trimzero(val)  if re.search(rxlist[1],val,flags=0) else val for val in values  ] # Don't do that for ADD
                    _logger.info('** return res**:%s', res)
            _logger.info('---END OF IF---')
        else: break
    return res


def mergeADD2SCA(res):
    """Merge the ADD dict into the SCA dict
    
        res: dict coming from the map2odoofield method
        res: eg :{'A': {'add_od': '+9.00', 'add_os': '+9.00'}, 'a': {'add_od': '+5.00', 'add_os': '+5.00'}, 'F': {'sph_os': '+3.25', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}}
        
        return : dict {'F': {'sph_os': '+3.25', 'add_od': '+9.00', 'add_os': '+9.00', 'sph_od': '-0.75', 'cyl_od': '-3.00', 'axis_os': '100', 'axis_od': '150', 'cyl_os': '-7.75'}, 'f': {'sph_os': '+10.50', 'add_od': '+5.00', 'add_os': '+5.00', 'sph_od': '+7.75', 'cyl_od': '-5.00', 'axis_os': '100', 'axis_od': '65', 'cyl_os': '-5.50'}}
    """

    _logger.info('passing in MERGEANDSUBSTITUTE')
    _logger.info('res.keys():%s', res.keys())

    for key in res.keys():
        print 'key : {}'.format(key)
        if key == 'A' :
            if 'F' in res.keys():
                print "before update:{}".format(res)
                res['F'].update(res[key])
                print 'after update: {}'.format(res)
                res.pop(key)
                print 'after pop:{}'.format(res)
                # res[mapvatype['F']] = res.pop('F')
        if key == 'a':
            if 'f' in res.keys():
                res['f'].update(res[key])
                res.pop(key)
                # res[mapvatype['f']] = res.pop('f')
    return res

def substitute(res):
    """Substitute keys (f,F,N,n)with selection values from Odoo
    
    res : dict return by mergeADD2SCA
    
    return : dict 
    return eg: 
    """
    _logger.info('in substitute method')
    _logger.info('res is:%s', res)
    _logger.info('res.keys:%s', res.keys())

    for key in res.keys():
        res[mapvatype[key]] = res.pop[key]
    _logger.info('in substitute return :%s', res)
    return res

def map2odoofields(values):
    """Map datas to ODOO field names
    
    values list of datas from rt5100 after parsing
    values eg: [['AL', '+6.50'], ['AR', '+1.50'], ['FL', '-2.00', '0.00', '0'], ['FR', '-2.00', '0.00', '9'], ['fL', '-3.00', '0.00', '0'], ['fR', '-3.00', '0.00', '0'],]
    values is returned by getandformat_values function
    """
    _logger.info('in map2fields')
    res = {}
    for item in values:  # 1ere pass on populate le dictionnary avec les clefs primaires : A, a , F, f....and empty dict
        res.update({item[0][0]:{}})
        _logger.info('first pass res is:%s', res)
    for item in values:  # on second : populate empty dict with datas.
        _logger.info('item is:%s', item)

        if re.search(r'[aA]', item[0][0], flags = 0):  # on est dans les additions. On peut mapper avec les champs d'addition
            if 'R' in item[0][1]:  # on est à droite
                print 'R:{}'.format(res[item[0][0]])
                res[item[0][0]].update({'add_od':item[1]})
                print 'res after R:{}'.format(res)
            if 'L' in item[0][1]:
                print res[item[0][0]]
                res[item[0][0]].update({'add_os':item[1]})

        if re.search(r'[fFnNO]', item[0], flags = 0):  # on est sur du SCA
            if 'R' in item[0]:
                res[item[0][0]].update({'sph_od':item[1],
                                        'cyl_od':item[2],
                                        'axis_od':item[3]
                                         })
            if 'L' in item[0]:
                res[item[0][0]].update({'sph_os':item[1],
                                        'cyl_os':item[2],
                                        'axis_os':item[3]
                                         })

        if re.search(r'[uUM]', item[0], flags = 0):  # extended visual acuity
            if 'R' in item[0]:  # on est à droite
                res[item[0][0]].update({'va_or_extended':item[1]})
            if 'L' in item[0]:  # on est à gauche
                res[item[0][0]].update({'va_ol_extended':item[1]})
            if 'B' in item[0]:  # on est en binoculaire
                res[item[0][0]].update({'va_bin_extended':item[1]})

        if re.search(r'[VvW]', item[0], flags = 0):  # non extended visual acuity
            if 'R' in item[0]:  # on est à droite
                res[item[0][0]].update({'va_or':item[1]})
            if 'L' in item[0]:  # on est à gauche
                res[item[0][0]].update({'va_ol':item[1]})
            if 'B' in item[0]:  # on est en binoculaire
                res[item[0][0]].update({'va_bin':item[1]})

    _logger.info('res is: %s', res)
    return res


if __name__ == '__main__':

    datas = getandformat_values()
    print 'getandformat_values return :{}'.format(datas)

    res = mergeandsubstitute(map2odoofields(datas))
    print "map2odoofields(datasV2, ) : {}".format(res)

#     res= mergeandsubstitute(res)
#     print 'mergeandsubstitute return : {}'.format(res)










    #===============================================================================
# mapvatype = {'a':'BCVA',
#                     'A':'Rx',
#                     'f':'BCVA',
#                     'F':'Rx',
#                     'n':'BCVA',
#                     'N': 'Rx',
#                     }
# mappedvatype = {'BCVA':('a', 'f', 'n'), 'Rx':('F', 'N', 'A')}
#
# for oldk in res.keys():  # mondict[newk]=mondict.pop([oldk])
#     print oldk
#     res[mapvatype[oldk]] = res.pop(oldk)
#     print res
#     print '---'
# print 'new res is: {}'.format(res)

# On ne peut pas simplementsubstituer les clefs 'A' 'a', 'f', 'n'.... avec les selections de odoo
# Pour cela il faut rentrer les ADD dans les SCA et ce n'est pas simple
# Essayons de rentrer le dictionnaire res dans les tables.
#===============================================================================

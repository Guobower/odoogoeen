# -*- coding: utf-8 -*-
import re
import os

SCAdict = {'f':('subjectdata', 'FarVisionSCA'),
              'n':('subjectdata', 'NearVisionSCA'),
              'F':('finalprescriptiondata', 'FarVisionSCA)'),
              'N':('finalprescriptiondata', 'NearVisionSCA'),
              'O':('ARdata', 'ObjectiveSCA'),
               }
keysOR = ('sph_od', 'cyl_od', 'axis_od')
keysOS = ('sph_os', 'cyl_os', 'axis_os')

# coupures peut changer si le programme qui crée le log avec les donnees du RT-5100 change.
coupures = [28, 30, 36, 42, 46]  # Les points de coupures semblent etre toujours les memes


# les données recherchées peuvent etre récupérée par l'index
# S=morceaux[1] C=morceaux[2] A=Morceaux[3]

def get_values(filter):
    """Return a dictionnary of the values
    
        filter(str) : the letter from the interface manual rs-232 of RT-5100
        Il y a un probleme quand il n'y a aucune ligne qui correspond au filtre
        log_path : path to the file with the datas given by RT-5100 device
        
        return : tuple .vals:({'cyl_od': '- 1.25', 'axis_od': '125', 'sph_od': '+ 5.50'}, {'sph_os': '+ 5.50', 'axis_os': '125', 'cyl_os': '- 1.25'})
    """
    log_name = 'tmp.log'
    log_path = os.path.join(os.path.expanduser('~'), 'rt5100rs232', log_name)

    filterR = filter + 'R'
    filterL = filter + 'L'

    if filter not in ['f', 'n', 'F', 'N', 'O']:
        print "print there is a problem with your filter:{}".format(filter)
        print "{} is not a code for RT-5100 datas".format(filter)
    else:
        try:
            file = open(log_path, 'r')

            for line in file.readlines():
                if line.find(filterR) != -1 or line.find(filterL) != -1:
                    morceaux = [line[i:j] for i, j in zip([0] + coupures, coupures + [None])]  # on coupe les lignes en morceaux qui isolent les champs.
                    values = morceaux[1:5]  # on élimine le champ date et on récupere que les champs datas.
                    print 'morceaux[1:5] : {}'.format(values)
                    # print '-' * 6
                    # print 'line:{}'.format(line)
                    # print 'morceaux:%s ' % (morceaux)
                    # print 'values:{}'.format(values)
                    # print '{} SCA:{},{},{}'.format(morceaux[1], morceaux[2], morceaux[3], morceaux[4])
                    if values[0] == filterR:  # On filtre pour l'oeil droit
                        valuesOD = dict(zip(keysOR, values[1:]))
                        # print 'valuesOD:{}'.format(valuesOD)
                    else:
                        valuesOS = dict(zip(keysOS, values[1:]))  # on filtre pour l'oeil gauche
                        # print 'valuesOS:{}'.format(valuesOS)

        except IOError, (error, strerror):
            print 'In log_path: {}'.format(log_path)
            print "I/O Error(%s): %s" % (error, strerror)

   # print 'locals():{}'.format(locals())
    # print 'done'
   # print '-'*10
    res = (valuesOD, valuesOS)
    return res

def trimspace(val):
    idx = 1
    val = val.strip()
    if val[1] == ' ':
        res = val[:idx] + val[(idx + 1):]
    else:
        res = val
    return res

def trimzero(val):
    res = val
    regex = r'\.\d0'
    if re.search(regex, val, flags = 0):
        match = re.search(regex, val, flags = 0)
        print 'match:{}'.format(match)
        if val[-1] == '0':
            res = val[:-1]
    return res

def main_trim(val):
    """ Apply trimzero and trimspace
    
        return: string the trimed val
    """
    print 'in main_trim val is {}'.format(val)
    res = trimspace(trimzero(val))
    print 'in main_trim res is {}'.format(res)
    return res

def main_get(vals):
    """Get the SCA values ready for ODOO
    
        vals tuple of dictionnaries from get values
        
        return: tuble of dictionnaryes of values trimed
    """
    for i in vals:
        for k, v in i.iteritems():
            i[k] = main_trim(v)
    return vals

if __name__ == '__main__':
    vals = get_values("O")
    print 'vals:{}'.format(vals)
    print 'OD:{}'.format(vals[0])
    print 'OG:{}'.format(vals[1])
    print 'Now trim values'
    print "main_get() : {}".format(main_get(vals))
    #===========================================================================
    # for i in SCAdict.keys():
    #     print '='*10
    #     get_values(i)
    #===========================================================================



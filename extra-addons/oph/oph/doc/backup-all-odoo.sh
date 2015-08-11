#! /bin/bash

#////////////////////////////////////////////////////////////////////////////////////#
# Script de sauvegarde complète d'OpenERP                                            #
# Par Thierry Godin : 2013-06-23                                                     #
# http://thierry-godin.developpez.com/                                               #
# derniere MAJ : 2013-11-25                                                          #
# modifié le : 22/07/2015 
# par laurent FRANCOIS                                                               #
# Le script effectue une sauvegarde complète des fichiers OpenERP                    #
# et du fichier de configuration du serveur openerp-server.conf                      #
# ainsi que de la base de données au format TAR                                      #
#                                                                                    #
# Sauvegarde en local dans le répertoire de l'utilisateur openerp                    #
#                                                                                    #
# Script à mettre en CHMOD : 0755                                                    #
# Et à exécuter en 'root'                                                            #
#                                                                                    #
#   Utilisation :                                                                    #
#   -------------                                                                    #
#   Pour exécuter le fichier sous Debian                                             #
#   Placer le fichier dans le répertoire /root                                       #
#   Ouvrir une invite de commande et entrer                                          #
#       cd /root                                                                     #
#       bash ./backup-all-odoo.sh                                                   #
#                                                                                    #      
#////////////////////////////////////////////////////////////////////////////////////#

# ---------------------------------------------------------------------------------- #
# !!!                                IMPORTANT                                     !!!
# ---------------------------------------------------------------------------------- #
#                                                                                    #
# Modifier le fichier pg_hba.conf de PostgreSQL pour autoriser la connexion          #
# sans mot de passe en local                                                         #
#                                                                                    #
# Emplacement du fichier = /etc/postgresql/9.1/main/pg_hba.conf :                    #
# Rajouter ou modifier la ligne ci-dessous :                                         #
#                                                                                    #
# TYPE  DATABASE        USER            ADDRESS                 METHOD               #
# local   all          openerp                                  trust                #
#                                                                                    #
# ---------------------------------------------------------------------------------- #

# Fichier de LOG
LOG_FILE='/var/log/openerp/odoo_backup.log'

# Création du fichier de log
if [ ! -e ${LOG_FILE} ]; then
    echo 'Creation du fichier de log :'${LOG_FILE}
    touch ${LOG_FILE}
fi

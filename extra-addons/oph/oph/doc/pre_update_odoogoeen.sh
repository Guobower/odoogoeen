#! /bin/bash

#////////////////////////////////////////////////////////////////////////////////////#
# Script for backup of the production version of odoogoeen
# to be run before an update                                                         #
#                                                                                    #
# derniere MAJ :                                                                     #
# Created : 06/08/2015 
# par laurent FRANCOIS                                                               #
# Le script effectue une sauvegarde complète du repertoire odoogoeen
# So there is a problem during update you can reverse easily                         #
# without usint git.
# 
# In this backup you have the last filestore                                         #
# with all the docs, odt, pdf ... for patients                                       #
#                                                                                    #
# Script à mettre en CHMOD : 0755 je ne sais pas                                     #
# Et à exécuter sur le server en 'root' je ne sais pas                               #
#                                                                                    #
#   Utilisation :                                                                    #
#   -------------                                                                    #
#   Pour exécuter le fichier sous Debian 
#   ssh to the server
#   Placer le fichier dans le répertoire /root                                       #
#   Ouvrir une invite de commande et entrer                                          #
#       cd /root                                                                     #
#       bash ./       
#                                                                                    #
#                                                                                    #      
#////////////////////////////////////////////////////////////////////////////////////#

# ---------------------------------------------------------------------------------- #
NOW = $(date+"%F-%T)
HOMEDIR='/home/lof' # home directory in the odoo server
SERVERDIR='/home/lof/ODOO'
SERVERDIRNAME='odoogoeen'
BCKDIR='odoogoeen.last.prod'
# ----------------------------------------------------------------------------------- #
echo "--- WARNING --- WARNING ---"
echo "we are closing the odoogoeen server"
service odoo-server stop

echo "Backing up the last running odoogoeen directory of the server, please wait..."
rsync-copy $SERVERDIR/$SERVERDIRNAME/ $HOMEDIR/$BCKDIR.$NOW

Echo "The last odoogoeen server directories are:"
ls -alh $HOMEDIR/$BCKDIR*

Echo "Size of the last backup odoogoeen directories are:"
du -h --summarize HOMEDIR/BCKDIR*/

Echo "The size of filestore directory is:"
du -h --summarize $SERVERDIR/$SERVERDIRNAME/openerp/filestore

Echo "Now we are updating the production server directory"
Echo "Renaming the production server directory to $SERVERDIRNAME.last"
mv $SERVERDIR/$SERVERDIRNAME $SERVERDIR/$SERVERDIRNAME.last
ls -alh $SERVERDIR/$SERVERDIRNAME

Echo "Update the odoo server directory from $HOMEDIR/$SERVERDIRNAME to $SERVERDIR"
rsync-move $HOMEDIR/$SERVERDIRNAME $SERVERDIR/
ls -alh $SERVERDIR/$SERVERDIRNAME



Echo "change ownership and group to $ODOOUSER"
chown -R $ODOOUSER:$ODOOUSER $SERVERDIR/$SERVERDIRNAME/

Echo "Restart the server odoogoeen"
service odoo-server start
tail -f /var/log/openerp/odoo-server.log
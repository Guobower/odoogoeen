#!/bin/bash
#update the version of odoo
#Utiliser des chemins absolu pour les dossiers et des chemins relatif pour les nom de 
#$CHEMIN_DU_DOSSIER/$NOM_DU_FICHIER
#
#suffixe=$(date +%F_%T) ---> 2015-02-07_10:20:37
#cp -a /home/lfs/odoogoeen /usr/odoogoeen-$(date +F_%T)

#sudo
#user host=(as user) [NOPWD:] cmd
#1er arg : user
#2eme arg: machine sur lequel le droit de la ligne sont valables
#3eme arg: utilisateur dont root prend les droits
#4eme arg: les commandes aux quelles user aura droit

SERVER_DIR=/usr
echo "SERVER:$SERVER_DIR"
CURRENT_USER=lof
DIR_NAME=odoogoeen.source
REPOSITORY=/home/$CURRENT_USER/$DIR_NAME
PROD_BRANCH=devfromscratch70
UPSTREAM=upstream
SERVER_PATH=/usr/odoo
SERVER_NAME=odoogoeen
SUFFIXE=$(date +'%F_%T')

echo "SUFFIXE: $SUFFIXE"

error() {
	printf '\E[31m'; echo "$@"; printf '\E[0m'
}
#check if you're root
#not useful here
#in case I need it
if [[ "$EUID" -eq 0 ]]; then
	error "This script should be run using sudo or as the root user"
	exit 1
fi

## STOP SERVICE
sudo service odoo-server stop

#test sur les symbolic link
[ -h  $SERVER_PATH/$SERVER_NAME -a -e $SERVER_PATH/$SERVER_NAME ]  && echo "foo existe. je le supprime " || echo "foo n'existe pas"

#manage filestorage
#before changing symlink
#trying to get the right PATH to the right FILESTORAGE
if [ -h  $SERVER_PATH/$SERVER_NAME ]
then 
	cd $SERVER_PATH/
	cd $SERVER_NAME
	TARGET=`pwd -P`
	echo "TARGET is: $TARGET"
else
	echo "Le symlink n'existe pas"
fi
#manage symlink
#shutdown service
#sudo service odoo-server stop
if [ -h  $SERVER_PATH/$SERVER_NAME ]
then 
	echo "$SERVER_PATH/$SERVER_NAME is a link"
	echo "I delete it"
	sudo unlink $SERVER_PATH/$SERVER_NAME
	echo "symlink deleted"
	echo "Create symlink to the right server name: $SERVER_NAME.$SUFFIXE"
	sudo ln -s $SERVER_PATH/$SERVER_NAME.$SUFFIXE $SERVER_PATH/$SERVER_NAME
	
else
	echo "$SERVER_PATH/$SERVER_NAME is not a link"
	echo "Create symlink $SERVER_PATH/$SERVER_NAME"
	sudo ln -s $SERVER_PATH/$SERVER_NAME.$SUFFIXE $SERVER_PATH/$SERVER_NAME
fi
#start service odoo-server
#sudo service odoo-server start
	
# on met à jour le repository
# doit se faire sous le current user
echo "Pull github $PROD_BRANCH"
echo "Change directory to $REPOSITORY"
cd $REPOSITORY
git checkout $PROD_BRANCH
git pull $UPSTREAM $PROD_BRANCH 
echo "C'est fait"
#Verification de l'existance du dir contenant le serveur
if [ -d $SERVER_PATH ]; then
	#exit 1
	sudo rsync -avh $REPOSITORY/ /usr/odoo/odoogoeen.$SUFFIXE
else
	#exit 1
	sudo mkdir $SERVER_PATH
	rsync -avh $REPOSITORY/ $SERVER_PATH/$SERVER_NAME.$SUFFIXE
fi

## chown -R openerp:openerp /usr/odoogoeen

###on récupere tout le filestorage.
#rsync -avh /usr/odoogoeen.16022015/openerp/filestore /usr/odoogoeen/openerp

## Start the server
sudo service odoo-server start
exit 0
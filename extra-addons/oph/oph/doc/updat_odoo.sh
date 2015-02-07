#!/bin/bash
#update the version of odoo
#mùùùmùùù
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
SUFFIXE=$(date +'%F_%T')
echo "SUFFIXE: $SUFFIXE"

error() {
	printf '\E[31m'; echo "$@"; printf '\E[0m'
}
#check if you're root
if [[ "$EUID" -eq 0 ]]; then
	error "This script should be run using sudo or as the root user"
	exit 1
fi


# on met à jour le repository
# doit se faire sous le current user
echo "Pull github $PROD_BRANCH"
echo "Change directory to $REPOSITORY"
cd $REPOSITORY
git checkout $PROD_BRANCH
git pull $UPSTREAM $PROD_BRANCH 
echo "C'est fait"
#Verification de l'existance du dir contenant le serveur
if [ -d /usr/odoo ]; then
	#exit 1
	sudo rsync -avh $REPOSITORY/ /usr/odoo/odoogoeen.$SUFFIXE
else
	#exit 1
	sudo mkdir /usr/odoo
	rsync -avh $REPOSITORY/ /usr/odoo/odoogoeen.$SUFFIXE
fi

exit 0;
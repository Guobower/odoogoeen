#!/bin/bash 
# openoffice.org headless server script 
# 
# chkconfig: 2345 80 30 
# description: headless libreoffice server script 
# processname: libreoffice 
# 
# Author: Vic Vijayakumar 
# Modified by Federico Ch. Tomasczik 
# 
# save this file
# move the file to /etc/init.d
#sudo chmod +x /etc/init.d/libreoffice.sh
#sudo chmod 0755 /etc/init.d/openoffice.sh
#sudo update-rc.d libreoffice.sh defaults

OOo_HOME=/usr/bin 
SOFFICE_PATH=$OOo_HOME/libreoffice 
PIDFILE=/var/run/libreoffice-server.pid 

set -e 

case "$1" in 
start) 
if [ -f $PIDFILE ]; then 
echo "LibreOffice headless server has already started." 
sleep 5 
exit 
fi 
echo "Starting LibreOffice headless server" 
$SOFFICE_PATH --nologo --nofirststartwizard --headless --norestore --invisible "--accept=socket,host=localhost,port=8100,tcpNoDelay=1;urp;" & > /dev/null 2>&1 
touch $PIDFILE 
;; 
stop) 
if [ -f $PIDFILE ]; then 
echo "Stopping LibreOffice headless server." 
killall -9 oosplash && killall -9 soffice.bin 
rm -f $PIDFILE 
exit 
fi 
echo "LibreOffice headless server is not running." 
exit 
;; 
restart) 
$0 stop 
sleep 1 
$0 start 
;; 
*) 
echo "Usage: $0 {start|stop|restart}" 
exit 1 
esac 
exit 0
#!/bin/sh

#
# */5 * * * * /home/mumalab/display.sh
#


HOST=signman.intern.munichmakerlab.de
NODE=$(ip a | grep "link/ether" | awk '{print $2}' | tr -d ":")
CONFIG_URL=http://$HOST/api/v1/config/$NODE

DISPLAY_URL=$(curl -s $CONFIG_URL | grep -e "^URL" | awk '{print $2}')

BROWSER_PID=$(pgrep midori)
nohup midori --display=:0.0 -e Fullscreen -a $DISPLAY_URL > /dev/null 2>/dev/null &
sleep 1
kill $BROWSER_PID

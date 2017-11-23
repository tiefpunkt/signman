#!/bin/sh

# SignMan Digital Signage Client
#
# Crontab entry:
# */1 * * * * /home/signman/signman.sh
#

HOST=signs.munichmakes.de
CURRENT_SIGN_FILE=/tmp/signman_current

NODE_ID=$(ip a | grep "link/ether" | awk '{print $2}' | tr -d ":")
NODE_IP=$(ip -o a | grep "scope global" | awk '{print $4}')
CONFIG_URL=http://${HOST}/api/v1/config/${NODE_ID}?ipaddr=${NODE_IP}

CONFIG_FILE=$(mktemp)
curl -s -L ${CONFIG_URL} > ${CONFIG_FILE}

DISPLAY_URL=$(cat $CONFIG_FILE | grep -e "^URL" | awk '{print $2}')

rm ${CONFIG_FILE}

BROWSER_PID=$(pgrep midori)

if [ ! -e $CURRENT_SIGN_FILE ] || [ "`cat $CURRENT_SIGN_FILE`" != "$DISPLAY_URL" ] || [ ! "$BROWSER_PID" ]; then

    nohup midori --display=:0.0 -e Fullscreen -a $DISPLAY_URL > /dev/null 2>/dev/null &
    sleep 2
    kill $BROWSER_PID
    echo -n $DISPLAY_URL > $CURRENT_SIGN_FILE
fi

#!/bin/bash

APP_PATH=$(pwd)
echo "0 6,22 * * * root sleep \$[ ( \$RANDOM % 60 )  + 1 ]m && export \$(grep -v '^#' \$APP_PATH/.env.prod | xargs) && APP_PATH=$APP_PATH $APP_PATH/certbot/certbot_renew.sh" > /etc/cron.d/certbot-renew
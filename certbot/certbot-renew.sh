#!/bin/bash
echo "certbot $CERTBOT_DOMAIN renew" >> /var/log/certbot_renew.log
certbot certonly --non-interactive --manual --preferred-challenges=dns \
     --manual-auth-hook $APP_PATH/authenticator.sh \
     --manual-cleanup-hook $APP_PATH/auth_cleanup.sh \
     -d $CERTBOT_DOMAIN

     
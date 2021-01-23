#!/bin/bash
certbot certonly --non-interactive --manual --preferred-challenges=dns \
     --manual-auth-hook ${CERTBOT_SCRIPTS_PATH}/authenticator.sh \
     --manual-cleanup-hook ${CERTBOT_SCRIPT_PATH}/auth_cleanup.sh \
     -d ${CERTBOT_DOMAIN}
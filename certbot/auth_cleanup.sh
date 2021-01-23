#!/bin/bash

# Get your API key from https://www.cloudflare.com/a/account/my-account
#API_KEY

if [ -f /tmp/CERTBOT_$CERTBOT_DOMAIN/ZONE_ID ]; then
        DOMAIN=$(cat /tmp/CERTBOT_$CERTBOT_DOMAIN/ZONE_ID)
        echo Delete $DOMAIN
        rm -f /tmp/CERTBOT_$CERTBOT_DOMAIN/ZONE_ID
fi

# Remove the challenge TXT record from the zone
if [ -n "${DOMAIN}" ]; then
        curl -s -X DELETE "https://api.gandi.net/v5/livedns/domains/$DOMAIN/records/_acme-challenge.services/TXT" \
                -H "Authorization: Apikey $API_KEY" \
                -H "Content-Type: application/json"
fi
#!/usr/bin/env bash


# Get your API key from https://www.cloudflare.com/a/account/my-account
#API_KEY 

# Strip only the top domain to get the zone id
DOMAIN=$(expr match "$CERTBOT_DOMAIN" '.*\.\(.*\..*\)')

# Get the Cloudflare zone id
# ZONE_EXTRA_PARAMS="status=active&page=1&per_page=20&order=status&direction=desc&match=all"
# ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=$DOMAIN&$ZONE_EXTRA_PARAMS" \
#      -H     "X-Auth-Email: $EMAIL" \
#      -H     "X-Auth-Key: $API_KEY" \
#      -H     "Content-Type: application/json" | python -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")

# Create TXT record
CREATE_DOMAIN="_acme-challenge.$CERTBOT_DOMAIN"
RECORD_ID=$(curl -s -X PUT "https://api.gandi.net/v5/livedns/domains/$DOMAIN/records/_acme-challenge.services/TXT" \
                -H     "Authorization: Apikey $API_KEY" \
                -H     "Content-Type: application/json" \
                --data "{\"rrset_values\":[\"$CERTBOT_VALIDATION\"],\"rrset_ttl\":3600}"\
            )

    #  --data '{"rrset_values":"["'$CERTBOT_VALIDATION'"]","rrset_ttl":3600}') #
             #| python -c "import sys,json;print(json.load(sys.stdin)['message'])")
echo "{\"rrset_values\":[\"$CERTBOT_VALIDATION\"],\"rrset_ttl\":3600}"
echo $RECORD_ID

# Save info for cleanup
if [ ! -d /tmp/CERTBOT_$CERTBOT_DOMAIN ];then
        mkdir -m 0700 /tmp/CERTBOT_$CERTBOT_DOMAIN
fi
echo $DOMAIN > /tmp/CERTBOT_$CERTBOT_DOMAIN/ZONE_ID
# echo $RECORD_ID > /tmp/CERTBOT_$CERTBOT_DOMAIN/RECORD_ID

# Sleep to make sure the change has time to propagate over to DNS

sleep 25
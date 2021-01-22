#!/usr/bin/env bash
set -ue

# If we are passed arg flags then run against certbot certonly like an entrypoint
if [ "${1:0:1}" = '-' ]; then
 set -- certbot certonly "$@"
fi

# If crond is passed then check for certs
if [ "$1" = 'crond' ]; then

  # Get env vars
  if [ -z "${LE_EMAIL:-}" ]; then
    echo "LE_EMAIL environment variable is not set! Please set this to an an email address you control."
    exit 1
  fi

  if [ -z "${LE_TEST:-}" ]; then
    declare -r LE_TEST='n'
  fi

  # Get all domain ENV vars
  ENVDomains=`env | sort | awk -F "=" '{print $1}' | grep "LE_DOMAIN_.*" || true`

  # Get all domains that certbot has certificates for in this volume
  CertBotDomains=`certbot -n certificates | grep "Domains:" || true`

  # Make sure there is at least one domain ENV var set
  if [ -z "${ENVDomains:-}" ]; then
    echo "WARNING: no LE_DOMAIN_* variables found! Certificates cannot be generated!"
    echo "Checking for existing certificates..."

    # If not, and certbot doesn't have any certs either, then exit as no action is possible
    if [ -z "${CertBotDomains:-}" ]; then
      echo "ERROR: no exising certificate(s) found and LE_DOMAIN_* is not set!"
      echo "Exiting as no certificats can be generated and there are none to renew!"
      echo "Please check the LE_DOMAIN_* environment variables and configure for your domain(s)."
      exit 1
    # If not, but certbot has existing certs, then just run crond
    else
     echo "Tailing logfile..."
     (umask 0 && truncate -s0 /var/log/letsencrypt/letsencrypt.log )
     tail --pid $$ -n0 -F /var/log/letsencrypt/letsencrypt.log &
     echo "Existing certificate(s) found. Running crond."
     exec "$@"
    fi
  # If domain ENV vars exist, loop through them
  else
    echo "$ENVDomains" | while IFS= read -r DomainVar ; do

      # If current ENV var is empty, just move on
      if [ -z "${!DomainVar}" ]; then
        echo "$DomainVar is not set, continuing..."
        continue
      # If not empty, check to see if certbot already has a certificate for the domain
      else
        case "$CertBotDomains" in
          *"${!DomainVar}"* )
            # If certbot already has a cert for this domain, move on
            echo "Found existing certificate for ${!DomainVar}, continuing..."
            continue
          ;;
          * )
            # If not, try to generate certs with the config given
            echo "No existing certificate found for ${!DomainVar}, attempting to generate one..."

            # Generate normal certificate
            if [ "$LE_TEST" = "n" ]; then
              certbot certonly --webroot -w $LE_WEBROOT -d "${!DomainVar}" --email "$LE_EMAIL" --agree-tos --non-interactive --keep-until-expiring --rsa-key-size 4096 --hsts --uir --preferred-challenges http

              echo "Certificate generated. Pausing and continuing..."
              sleep 2
              continue

            # Generate test certificate
            elif [ "$LE_TEST" = "y" ]; then
              echo "NOTE: TEST certificate(s) requested. Generating test certificate instead..."
              certbot certonly --webroot -w $LE_WEBROOT -d "${!DomainVar}" --email "$LE_EMAIL" --agree-tos --non-interactive --keep-until-expiring --rsa-key-size 4096 --hsts --uir --preferred-challenges http --test-cert --debug-challenges

              echo "Certificate generated. Pausing and continuing..."
              sleep 2
              continue

            # If LE_TEST was set to something else, exit as we don't know what the user wants
            else
              echo "LE_TEST has been set to: $LE_TEST"
              echo "You must set LE_TEST to 'y' if you want to generate a test certificate, or 'n' to generate a valid one!"
              echo "LE_TEST defaults to 'n' if unset."
              echo "Exiting"
              exit 1
            fi
          ;;
        esac
      fi
    done
    # Re-check cerbot domains to make sure there is now at least one certificate
    sleep 2
    CertBotDomains=`certbot -n certificates | grep "Domains:" || true`
    if [ -z "${CertBotDomains:-}" ]; then
      echo "ERROR: no certificates were generated!"
      echo "Exiting as there are no cerficates to renew!"
      echo "Please check the LE_DOMAIN_* environment variables and configure for your domain(s)."
      exit 1
    # If there is now at least one certificate known to certbot, we can run crond
    else
      echo "Existing certificates detected."
      echo "Tailing logfile..."
      (umask 0 && truncate -s0 /var/log/letsencrypt/letsencrypt.log )
      tail --pid $$ -n0 -F /var/log/letsencrypt/letsencrypt.log &
      echo "Running crond."
      exec "$@"
    fi
  fi
fi

# If other command, just run it
exec "$@"

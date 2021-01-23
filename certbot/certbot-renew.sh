#!/bin/bash
certbot certonly --non-interactive --manual --preferred-challenges=dns --manual-auth-hook \
     ./authenticator.sh --manual-cleanup-hook ./auth_cleanup.sh -d services.ozuevo.top
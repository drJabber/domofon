# le-certbot

Cerbot docker container based on Alpine Linux.

This container will automate the generation of letsencrypt certificates using certbot, and will run 'certbot renew' with crond to automatically renew them when they are close to expiring.

## How to use

This image can be used in two main ways:

### With a companion webserver

Please see [le-docker](https://github.com/snw35/le-docker) for the docker-compose file that will automatically deploy this image alongside the [le-nginx](https://github.com/snw35/le-nginx) proxy container.

The [le-nginx](https://github.com/snw35/le-nginx) proxy has been configured to redirect all traffic to port 443 (HTTPS) while still allowing through the letsencrypt challenges.

### Standalone

This container runs 'certbot certonly' as its default entry-point. You can pass arguments directly to it, or simply run it like this:
```
docker run -it --mount source=le-certs,target=/etc/letsencrypt -p 80:80 -p 443:443 snw35/le-certbot --standalone
```
This will allow you to interactively obtain certificates and store them inside the le-certs named volume. If you then run the container with the volume mounted, it will detect your existing certificates and revert to running crond with 'certbot renew':
```
docker run -it --mount source=le-certs,target=/etc/letsencrypt -p 80:80 -p 443:443 snw35/le-certbot
```
You can then mount the le-certs volume into your own containers to use the certificates at /etc/letsencrypt/(your domain)/live.

***

 * [Travis CI: ![Build Status](https://travis-ci.org/snw35/le-certbot.svg?branch=master)](https://travis-ci.org/snw35/le-certbot)

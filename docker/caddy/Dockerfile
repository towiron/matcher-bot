FROM caddy:2.6.2-builder-alpine AS builder

FROM caddy:2.6.2-alpine AS local

WORKDIR /var/www
COPY ./Caddyfile.prod /etc/caddy/Caddyfile
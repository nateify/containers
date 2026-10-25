# renovate: datasource=docker depName=caddy versioning=semver
ARG CADDY_VERSION=2.11.7

# renovate: datasource=github-releases depName=caddy-dns/cloudflare versioning=semver
ARG CLOUDFLARE_PLUGIN_VERSION=v0.2.4

FROM caddy:${CADDY_VERSION}-builder-alpine AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare@${CLOUDFLARE_PLUGIN_VERSION}

# renovate: datasource=docker depName=alpine versioning=semver
FROM alpine:3.24.3

RUN apk add --no-cache \
    ca-certificates \
    curl \
    libcap \
    mailcap \
    tini \
    tzdata

RUN set -eux; \
    mkdir -p \
        /config/caddy \
        /data/caddy \
        /etc/caddy \
        /srv \
    ; \
    chmod 1777 /config/caddy /data/caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

RUN setcap cap_net_bind_service=+ep /usr/bin/caddy; \
    chmod +x /usr/bin/caddy; \
    caddy version

ENV XDG_CONFIG_HOME=/config
ENV XDG_DATA_HOME=/data

WORKDIR /srv

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]

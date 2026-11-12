# renovate: datasource=docker depName=caddy versioning=semver
ARG CADDY_VERSION=2.11.9

# renovate: datasource=github-releases depName=caddy-dns/cloudflare versioning=semver
ARG CLOUDFLARE_PLUGIN_VERSION=v0.2.4

FROM caddy:${CADDY_VERSION}-builder-alpine AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare@${CLOUDFLARE_PLUGIN_VERSION}

RUN mkdir -p \
    /config/caddy \
    /data/caddy \
    /etc/caddy \
    /srv && \
    touch /etc/caddy/Caddyfile && \
    chown -R 65532:65532 /config /data /etc/caddy /srv

FROM gcr.io/distroless/static-debian13:nonroot

COPY --from=builder /build/caddy /usr/bin/caddy

COPY --from=builder --chown=65532:65532 /config /config
COPY --from=builder --chown=65532:65532 /data /data
COPY --from=builder --chown=65532:65532 /etc/caddy /etc/caddy
COPY --from=builder --chown=65532:65532 /srv /srv

ENV XDG_CONFIG_HOME=/config
ENV XDG_DATA_HOME=/data

WORKDIR /srv
USER 65532:65532

EXPOSE 80 443 2019
EXPOSE 443/udp

ENTRYPOINT ["/usr/bin/caddy"]
CMD ["run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]

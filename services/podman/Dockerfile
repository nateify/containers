ARG ALMA_VERSION=10.2-20261027

FROM docker/compose-bin:v5.6.1 AS compose-bin

FROM ghcr.io/almalinux/10-minimal:${ALMA_VERSION}

# renovate: datasource=github-releases depName=krallin/tini
ARG TINI_VERSION="v0.19.0"

RUN microdnf install -y \
    podman \
    podman-docker \
    shadow-utils \
    curl-minimal && \
    microdnf clean all

RUN ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/') && \
    curl -fsSL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${ARCH}" -o /usr/bin/tini && \
    chmod +x /usr/bin/tini

COPY --from=compose-bin /docker-compose /usr/local/bin/docker-compose

RUN chmod +x /usr/local/bin/docker-compose && \
    mkdir -p /usr/libexec/docker/cli-plugins /root/.docker/cli-plugins && \
    ln -s /usr/local/bin/docker-compose /usr/libexec/docker/cli-plugins/docker-compose && \
    ln -s /usr/local/bin/docker-compose /root/.docker/cli-plugins/docker-compose

ENV DOCKER_HOST="unix:///run/podman/podman.sock"

RUN mkdir -p /run/podman /var/lib/containers /etc/containers

RUN cat <<'EOF' > /etc/containers/containers.conf
[containers]
label = false
log_driver = "k8s-file"
log_size_max = 10485760

[engine]
cgroup_manager = "cgroupfs"
events_logger = "file"
events_logfile_max_size = "5m"
service_timeout = 0
EOF

RUN cat <<'EOF' > /etc/containers/storage.conf
[storage]
driver = "overlay"
EOF

VOLUME /var/lib/containers

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["podman", "system", "service", "--time=0", "unix:///run/podman/podman.sock"]

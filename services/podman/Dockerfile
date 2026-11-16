ARG ALMA_VERSION=10.2-20261114

FROM docker/compose-bin:v5.7.1 AS compose-bin

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
RUN echo 'export DOCKER_HOST="unix:///run/podman/podman.sock"' > /etc/profile.d/docker_host.sh && \
    echo 'DOCKER_HOST="unix:///run/podman/podman.sock"' >> /etc/environment

RUN mkdir -p /run/podman /var/lib/containers /var/lib/volumes /etc/containers

RUN touch /etc/containers/nodocker

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
volume_path = "/var/lib/volumes"
EOF

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]
CMD ["podman", "system", "service", "--time=0", "unix:///run/podman/podman.sock"]

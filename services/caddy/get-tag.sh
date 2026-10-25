#!/usr/bin/env bash
set -euo pipefail

get_docker_ver() {
    sed -nE "s/^[[:blank:]]*$1[=:]([[:blank:]]*\"?v?)([^\"'[:space:]]+).*/\2/p" Dockerfile | head -n1
}

CADDY_VER=$(get_docker_ver 'ARG CADDY_VERSION')
CF_VER=$(get_docker_ver 'ARG CLOUDFLARE_PLUGIN_VERSION')
ALPINE_VER=$(get_docker_ver 'FROM alpine')

echo "${CADDY_VER}-cf${CF_VER}-alpine${ALPINE_VER}"

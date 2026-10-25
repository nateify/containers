#!/usr/bin/env bash
set -euo pipefail

CADDY_VER=$(grep -m1 'ARG CADDY_VERSION=' Dockerfile | cut -d= -f2 | tr -d '"\r ')
CF_VER=$(grep -m1 'ARG CLOUDFLARE_PLUGIN_VERSION=' Dockerfile | cut -d= -f2 | tr -d '"\r ')
ALPINE_VER=$(grep -m1 'FROM alpine:' Dockerfile | cut -d: -f2 | tr -d '\r ')

echo "${CADDY_VER}-cf${CF_VER}-alpine${ALPINE_VER}"

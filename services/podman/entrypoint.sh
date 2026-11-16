#!/bin/sh
set -e

if ! grep -qs '/run tmpfs' /proc/mounts; then
    mount -t tmpfs -o rw,nosuid,nodev,mode=755 tmpfs /run 2>/dev/null || true
fi

mkdir -p /run/podman

ln -sf /run/podman/podman.sock /run/docker.sock

exec "$@"

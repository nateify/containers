# renovate: datasource=github-releases depName=Brainicism/bgutil-ytdlp-pot-provider
ARG BGUTIL_VERSION="2.0.2"

FROM cgr.dev/chainguard/wolfi-base AS deps-prod
WORKDIR /app

RUN apk add --no-cache nodejs-26 npm

COPY package.json package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev --no-audit --no-fund

FROM cgr.dev/chainguard/wolfi-base AS build
WORKDIR /app

RUN apk add --no-cache nodejs-26 npm

COPY package.json package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

COPY tsconfig.json ./
COPY types/ types/
COPY src/ src/

RUN npx tsc

FROM cgr.dev/chainguard/wolfi-base AS runner
WORKDIR /app

RUN apk add --no-cache \
    nodejs-26 \
    fontconfig \
    ttf-dejavu && \
    mkdir -p /app && \
    chown -R nonroot:nonroot /app

COPY --from=deps-prod --chown=nonroot:nonroot /app/node_modules ./node_modules
COPY --from=build --chown=nonroot:nonroot /app/build ./build
COPY --chown=nonroot:nonroot package.json ./

ENV NODE_ENV=production

USER 65532:65532

EXPOSE 4416

ENTRYPOINT ["/usr/bin/node", "build/main.js"]
CMD ["--host", "0.0.0.0"]

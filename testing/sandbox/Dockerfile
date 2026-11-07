# Linux image for testing/sbx.sh when the host has no bubblewrap (a Mac).
# Build once, yourself, after Docker is already running. This repo does not build it.
#   docker build --platform linux/arm64 -t skillmaxx-sandbox:local -f testing/sandbox/Dockerfile testing/sandbox
# Free public base image and free npm CLIs. No model API key is used.
# Packages match testing/setup_agents.sh. Pi is @earendil-works/pi-coding-agent
# (the package the nightly sandbox actually runs; the old @mariozechner package is 0.73.1).
FROM node:22-bookworm
RUN apt-get update \
 && apt-get install -y --no-install-recommends git python3 ca-certificates curl bash \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/skillmaxx
RUN npm init -y \
 && npm i @anthropic-ai/claude-code @openai/codex @xai-official/grok @earendil-works/pi-coding-agent \
 && chmod -R a+rX /opt/skillmaxx
ENV HOME=/opt/cursorhome
RUN mkdir -p /opt/cursorhome \
 && curl -fsSL https://cursor.com/install | bash \
 && chmod -R a+rX /opt/cursorhome
ENV PATH="/opt/skillmaxx/node_modules/.bin:/opt/cursorhome/.local/bin:/usr/local/bin:/usr/bin:/bin"
WORKDIR /home/sbx

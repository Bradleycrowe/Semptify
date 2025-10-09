FROM mcr.microsoft.com/devcontainers/python:3.13

# Install Podman and related rootless tooling
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         podman uidmap slirp4netns fuse-overlayfs containers-common \
         shellcheck ca-certificates curl tar jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pre-create podman config directory for the vscode user (created by base image)
USER vscode
RUN mkdir -p /home/vscode/.config/containers && \
    printf '[engine]\nhelper_binaries_dir="/usr/bin"\n' > /home/vscode/.config/containers/engine.conf
USER root

# Helpful env defaults for rootless podman inside dev container
ENV PODMAN_IGNORE_CGROUPSV2_WARNING=1 \
    PODMAN_USERNS=keep-id

# Install podman-compose (Python wrapper) for compose-like workflows
RUN pip install --no-cache-dir podman-compose

# Install hadolint and actionlint
RUN curl -sL https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 -o /usr/local/bin/hadolint \
    && chmod +x /usr/local/bin/hadolint \
    && curl -sL https://github.com/rhysd/actionlint/releases/download/v1.7.1/actionlint_Linux_x86_64.tar.gz | tar xz -C /usr/local/bin actionlint

# Install Trivy and Syft (pinned versions)
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.55.0 \
    && curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin v1.19.0

# Retain original functionality provided via postCreateCommand in devcontainer.json
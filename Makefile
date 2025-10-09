# Makefile providing convenience targets for Docker and Podman
# Usage examples:
#   make build          (docker build)
#   make build PODMAN=1 (podman build)
#   make run            (run container mapping 8080)
#   make shell          (enter running container shell)
# Variables:
#   TAG?=dev
#   PODMAN?=0  (set to 1 to use podman)
#   IMAGE?=semptifygui

PODMAN?=0
ENGINE=$(if $(filter 1,$(PODMAN)),podman,docker)
IMAGE?=semptifygui
TAG?=dev
PORT?=8080
CONTAINER?=$(IMAGE)-$(TAG)

.PHONY: build run stop rm shell logs sbom trivy clean help

help:
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk -F':|##' '{printf "\033[36m%-15s\033[0m %s\n",$$1,$$3}'

build: ## Build image (ENGINE variable selects docker/podman)
	$(ENGINE) build -t $(IMAGE):$(TAG) .

run: stop ## Run container (detached)
	$(ENGINE) run -d --name $(CONTAINER) -p $(PORT):8080 $(IMAGE):$(TAG)

stop: ## Stop container if running
	-$(ENGINE) stop $(CONTAINER) >/dev/null 2>&1 || true
	-$(ENGINE) rm $(CONTAINER) >/dev/null 2>&1 || true

shell: ## Exec into running container
	$(ENGINE) exec -it $(CONTAINER) /bin/sh || $(ENGINE) exec -it $(CONTAINER) /bin/bash || true

logs: ## Tail container logs
	$(ENGINE) logs -f $(CONTAINER)

rm: stop ## Remove image
	-$(ENGINE) rmi $(IMAGE):$(TAG) || true

sbom: ## Generate SBOM with Syft (container must be built); requires syft installed
	which syft >/dev/null 2>&1 || (echo "Syft not installed" >&2; exit 2)
	syft $(IMAGE):$(TAG) -o json > sbom.json
	@echo "SBOM written to sbom.json"

trivy: ## Run Trivy scan (image must exist); requires trivy installed
	which trivy >/dev/null 2>&1 || (echo "Trivy not installed" >&2; exit 2)
	trivy image --severity CRITICAL,HIGH $(IMAGE):$(TAG)

clean: stop ## Remove image and artifacts
	-$(ENGINE) rmi $(IMAGE):$(TAG) || true
	-rm -f sbom.json

# Convenience target for podman build: make podman PODMAN=1
podman: ## Build using podman explicitly (alias for build with PODMAN=1)
	$(MAKE) build PODMAN=1

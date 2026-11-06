
if [ -f README.md ]; then
  echo "README.md already exists. Review it before making changes."
else
  cat > README.md <<'EOF'
# Enterprise AI Platform

## Overview
Production-oriented, multi-tenant AI Platform built on AWS.

## Goals
- Secure and scalable AI infrastructure
- Enterprise RAG applications
- Automated CI/CD and GitOps
- AI model serving and inference
- Production monitoring and SRE
- Load testing and incident simulations

## Technology Stack
- Cloud: AWS
- Infrastructure: Terraform
- Containers: Docker
- Orchestration: Kubernetes / EKS
- CI/CD: GitHub Actions / Argo CD
- Backend: Python / FastAPI
- AI: Amazon Bedrock / RAG / vLLM
- Monitoring: Prometheus / Grafana / OpenTelemetry
- Load Testing: k6

## Repository Structure
- infra/          Infrastructure as Code
- apps/           Application services
- platform/       Kubernetes and GitOps
- observability/  Metrics, logs and traces
- tests/          Automated and load tests
- docs/           Architecture and runbooks
- .github/        CI/CD workflows

## Environments
- Local
- Development
- Staging
- Production-like

## Security
Never commit credentials, secrets or Terraform state files.

## Status
Phase 1: Infrastructure Foundations
EOF
fi

git status --short --untracked-files=all


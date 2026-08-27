# AWS Deployment Reference

This directory contains a deployment **reference**, not a claim of a live AWS deployment.

A production AWS implementation should place the API in a managed container runtime, use managed PostgreSQL with pgvector where supported by the selected service/version, store secrets in a managed secrets service, and place public ingress behind TLS and appropriate network controls.

## Required production decisions

- AWS account and region
- container runtime (ECS/Fargate, EKS, or equivalent)
- managed PostgreSQL/pgvector compatibility
- VPC/private subnets/security groups
- Secrets Manager or equivalent
- TLS certificate and DNS
- logging/metrics destination
- backup/restore policy
- scaling and budget limits

No live deployment is represented by this repository until an actual AWS environment is provisioned and exercised.

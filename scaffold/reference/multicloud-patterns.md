# Multi-Cloud Patterns

Purpose: Use this file when you need Azure, Pulumi, or cross-cloud comparison instead of AWS- or GCP-only guidance.

Contents:
1. Provider comparison
2. Backend comparison
3. Minimal Azure/GCP snippets
4. Pulumi structure and commands

## Provider Comparison

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Network | VPC | VPC Network | VNet |
| Compute | EC2 / ECS / Lambda | Compute Engine / Cloud Run / Functions | VM / App Service / Functions |
| Database | RDS / Aurora / DynamoDB | Cloud SQL / Spanner / Firestore | Azure SQL / Cosmos DB |
| Kubernetes | EKS | GKE | AKS |
| Object storage | S3 | Cloud Storage | Blob Storage |
| Secrets | Secrets Manager | Secret Manager | Key Vault |
| Terraform state | S3 + DynamoDB | GCS | Azure Blob |

## Backend Comparison

| Backend | Typical use |
|---------|-------------|
| `s3` + lock table | AWS |
| `gcs` | GCP |
| `azurerm` | Azure |

## Minimal Snippets

### GCP backend

```hcl
terraform {
  backend "gcs" {
    bucket = "myproject-terraform-state"
    prefix = "dev/terraform.tfstate"
  }
}
```

### Azure backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "myprojecttfstate"
    container_name       = "tfstate"
    key                  = "dev/terraform.tfstate"
  }
}
```

## Pulumi Structure

```text
pulumi/
  Pulumi.yaml
  Pulumi.dev.yaml
  Pulumi.staging.yaml
  Pulumi.prod.yaml
  index.ts
  vpc.ts
  database.ts
```

Useful commands:

```bash
pulumi new aws-typescript
pulumi stack select dev
pulumi preview
pulumi up
pulumi destroy
pulumi import aws:ec2/vpc:Vpc main vpc-12345678
```

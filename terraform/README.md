# Salesforce Pipeline Terraform

Two independent root modules:
- `terraform/aws`: private dbt artifacts/docs bucket, private Salesforce CDC raw bucket, CloudFront OAC and GitHub OIDC.
- `terraform/snowflake`: Salesforce database, schemas, warehouses, RBAC, users, grants and Contact PII masking.

Copy each `terraform.tfvars.example` to `terraform.tfvars`, then run `terraform init`, `terraform fmt -check`, `terraform validate`, `terraform plan` from each module separately. Never commit tfvars or state files.

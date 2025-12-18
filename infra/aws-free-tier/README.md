# AWS Free Tier (Optional)

This module is not required for local usage. It provisions a single S3 bucket with versioning and an IAM policy for writing backups.

## Usage
```
terraform init
terraform apply -var suffix=uniquevalue
```

## Free tier notes
- S3 storage and requests are within the free tier limits for small backups.
- No compute resources are created.

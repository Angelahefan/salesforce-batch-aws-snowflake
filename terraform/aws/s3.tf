resource "aws_s3_bucket" "dbt_artifacts" {
  bucket = var.artifacts_bucket_name
  tags   = merge(local.common_tags, { Purpose = "dbt-artifacts-and-docs" })
}
resource "aws_s3_bucket_versioning" "dbt_artifacts" {
  bucket = aws_s3_bucket.dbt_artifacts.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "dbt_artifacts" {
  bucket = aws_s3_bucket.dbt_artifacts.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}
resource "aws_s3_bucket_public_access_block" "dbt_artifacts" {
  bucket = aws_s3_bucket.dbt_artifacts.id
  block_public_acls = true; block_public_policy = true; ignore_public_acls = true; restrict_public_buckets = true
}
resource "aws_s3_bucket_lifecycle_configuration" "dbt_artifacts" {
  bucket = aws_s3_bucket.dbt_artifacts.id
  rule {
    id = "cleanup-old-artifact-versions"; status = "Enabled"
    noncurrent_version_expiration { noncurrent_days = 30 }
  }
}
resource "aws_s3_bucket" "salesforce_raw" {
  bucket = var.salesforce_raw_bucket_name
  tags   = merge(local.common_tags, { Purpose = "salesforce-cdc-raw-data" })
}
resource "aws_s3_bucket_versioning" "salesforce_raw" {
  bucket = aws_s3_bucket.salesforce_raw.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "salesforce_raw" {
  bucket = aws_s3_bucket.salesforce_raw.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}
resource "aws_s3_bucket_public_access_block" "salesforce_raw" {
  bucket = aws_s3_bucket.salesforce_raw.id
  block_public_acls = true; block_public_policy = true; ignore_public_acls = true; restrict_public_buckets = true
}
resource "aws_s3_bucket_lifecycle_configuration" "salesforce_raw" {
  bucket = aws_s3_bucket.salesforce_raw.id
  rule {
    id = "abort-incomplete-multipart-uploads"; status = "Enabled"
    abort_incomplete_multipart_upload { days_after_initiation = 7 }
  }
}

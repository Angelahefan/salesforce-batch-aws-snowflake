output "artifacts_bucket_name" { value = aws_s3_bucket.dbt_artifacts.bucket }
output "salesforce_raw_bucket_name" { value = aws_s3_bucket.salesforce_raw.bucket }
output "github_actions_role_arn" { value = aws_iam_role.github_actions_cicd.arn }
output "cloudfront_distribution_id" { value = aws_cloudfront_distribution.docs.id }
output "dbt_docs_url" { value = "https://${aws_cloudfront_distribution.docs.domain_name}" }

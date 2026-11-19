resource "aws_cloudfront_origin_access_control" "docs" {
  name = "${var.project_name}-dbt-docs-oac"
  description = "OAC for private dbt docs bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior = "always"
  signing_protocol = "sigv4"
}
resource "aws_cloudfront_distribution" "docs" {
  enabled = true; default_root_object = "index.html"; comment = "dbt docs for ${var.project_name}"
  origin {
    domain_name = aws_s3_bucket.dbt_artifacts.bucket_regional_domain_name
    origin_id = "s3-dbt-docs"
    origin_path = "/docs"
    origin_access_control_id = aws_cloudfront_origin_access_control.docs.id
  }
  default_cache_behavior {
    allowed_methods = ["GET", "HEAD"]; cached_methods = ["GET", "HEAD"]
    target_origin_id = "s3-dbt-docs"; viewer_protocol_policy = "redirect-to-https"
    forwarded_values { query_string = false; cookies { forward = "none" } }
  }
  restrictions { geo_restriction { restriction_type = "none" } }
  viewer_certificate { cloudfront_default_certificate = true }
  tags = local.common_tags
}
data "aws_iam_policy_document" "cloudfront_access" {
  statement {
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.dbt_artifacts.arn}/docs/*"]
    principals { type = "Service"; identifiers = ["cloudfront.amazonaws.com"] }
    condition { test = "StringEquals"; variable = "AWS:SourceArn"; values = [aws_cloudfront_distribution.docs.arn] }
  }
}
resource "aws_s3_bucket_policy" "cloudfront_access" {
  bucket = aws_s3_bucket.dbt_artifacts.id
  policy = data.aws_iam_policy_document.cloudfront_access.json
}

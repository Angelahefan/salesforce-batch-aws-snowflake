resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
  tags = local.common_tags
}
data "aws_iam_policy_document" "github_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals { type = "Federated"; identifiers = [aws_iam_openid_connect_provider.github_actions.arn] }
    condition { test = "StringEquals"; variable = "token.actions.githubusercontent.com:aud"; values = ["sts.amazonaws.com"] }
    condition { test = "StringLike"; variable = "token.actions.githubusercontent.com:sub"; values = ["repo:${var.github_repository}:*"] }
  }
}
resource "aws_iam_role" "github_actions_cicd" {
  name = "${var.project_name}-github-actions-role"
  assume_role_policy = data.aws_iam_policy_document.github_assume_role.json
  tags = local.common_tags
}
data "aws_iam_policy_document" "github_permissions" {
  statement {
    sid = "DbtArtifacts"
    actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = ["${aws_s3_bucket.dbt_artifacts.arn}/*"]
  }
  statement {
    sid = "ListArtifactsBucket"; actions = ["s3:ListBucket"]; resources = [aws_s3_bucket.dbt_artifacts.arn]
  }
  statement {
    sid = "SalesforceRawObjects"
    actions = ["s3:GetObject", "s3:PutObject"]
    resources = ["${aws_s3_bucket.salesforce_raw.arn}/${var.raw_data_prefix}/*"]
  }
  statement {
    sid = "ListSalesforceRawPrefix"; actions = ["s3:ListBucket"]; resources = [aws_s3_bucket.salesforce_raw.arn]
    condition { test = "StringLike"; variable = "s3:prefix"; values = ["${var.raw_data_prefix}/*"] }
  }
  statement {
    sid = "InvalidateDocs"; actions = ["cloudfront:CreateInvalidation"]; resources = [aws_cloudfront_distribution.docs.arn]
  }
}
resource "aws_iam_role_policy" "github_actions" {
  name = "${var.project_name}-github-actions-policy"
  role = aws_iam_role.github_actions_cicd.id
  policy = data.aws_iam_policy_document.github_permissions.json
}

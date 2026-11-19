variable "aws_region" { type = string; default = "ap-southeast-2" }
variable "environment" { type = string; default = "dev" }
variable "project_name" { type = string; default = "salesforce-analytics" }
variable "artifacts_bucket_name" { type = string }
variable "salesforce_raw_bucket_name" { type = string }
variable "github_repository" { type = string }
variable "github_branch" { type = string; default = "main" }
variable "raw_data_prefix" { type = string; default = "raw/salesforce" }

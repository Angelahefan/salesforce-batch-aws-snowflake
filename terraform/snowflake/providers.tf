terraform {
  required_version = ">= 1.5.0"
  required_providers { snowflake = { source = "snowflakedb/snowflake", version = "~> 1.0" } }
}
provider "snowflake" {
  organization_name = var.snowflake_organization_name
  account_name = var.snowflake_account_name
  user = var.snowflake_admin_user
  password = var.snowflake_admin_password
  role = "ACCOUNTADMIN"
}

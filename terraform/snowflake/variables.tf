variable "snowflake_organization_name" { type = string }
variable "snowflake_account_name" { type = string }
variable "snowflake_admin_user" { type = string }
variable "snowflake_admin_password" { type = string; sensitive = true }
variable "database_name" { type = string; default = "SALESFORCE_ANALYTICS_DB" }
variable "warehouse_auto_suspend" { type = number; default = 60 }
variable "prod_dbt_password" { type = string; sensitive = true }
variable "cicd_user_password" { type = string; sensitive = true }
variable "gina_analyst_password" { type = string; sensitive = true }
variable "vicient_analyst_password" { type = string; sensitive = true }
variable "derek_analyst_password" { type = string; sensitive = true }

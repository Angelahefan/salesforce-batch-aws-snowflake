resource "snowflake_account_role" "admin" { name = "SALESFORCE_ADMIN" }
resource "snowflake_account_role" "transformer" { name = "SALESFORCE_TRANSFORMER" }
resource "snowflake_account_role" "analyst" { name = "SALESFORCE_ANALYST" }
resource "snowflake_grant_account_role" "admin_inherits_transformer" { role_name = snowflake_account_role.transformer.name; parent_role_name = snowflake_account_role.admin.name }
resource "snowflake_grant_account_role" "admin_inherits_analyst" { role_name = snowflake_account_role.analyst.name; parent_role_name = snowflake_account_role.admin.name }
resource "snowflake_grant_account_role" "sysadmin_inherits_admin" { role_name = snowflake_account_role.admin.name; parent_role_name = "SYSADMIN" }

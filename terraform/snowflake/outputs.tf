output "database_name" { value = snowflake_database.analytics.name }
output "warehouse_names" { value = { for size, wh in snowflake_warehouse.compute : size => wh.name } }
output "prod_dbt_user" { value = snowflake_user.prod_dbt.name }
output "cicd_user" { value = snowflake_user.cicd.name }
output "transformer_role" { value = snowflake_account_role.transformer.name }
output "analyst_role" { value = snowflake_account_role.analyst.name }
output "schemas" { value = local.prod_schemas }

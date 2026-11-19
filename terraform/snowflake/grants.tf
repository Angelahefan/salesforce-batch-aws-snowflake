resource "snowflake_grant_privileges_to_account_role" "transformer_wh" {
  for_each=toset(local.warehouse_sizes); account_role_name=snowflake_account_role.transformer.name; privileges=["USAGE","OPERATE"]
  on_account_object { object_type="WAREHOUSE"; object_name=snowflake_warehouse.compute[each.value].name }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_wh" {
  for_each=toset(local.warehouse_sizes); account_role_name=snowflake_account_role.analyst.name; privileges=["USAGE"]
  on_account_object { object_type="WAREHOUSE"; object_name=snowflake_warehouse.compute[each.value].name }
}
resource "snowflake_grant_privileges_to_account_role" "transformer_db" {
  account_role_name=snowflake_account_role.transformer.name; privileges=["USAGE","CREATE SCHEMA"]
  on_account_object { object_type="DATABASE"; object_name=snowflake_database.analytics.name }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_db" {
  account_role_name=snowflake_account_role.analyst.name; privileges=["USAGE"]
  on_account_object { object_type="DATABASE"; object_name=snowflake_database.analytics.name }
}
resource "snowflake_grant_privileges_to_account_role" "transformer_schema" {
  for_each=local.prod_schemas; account_role_name=snowflake_account_role.transformer.name; privileges=["USAGE","CREATE TABLE","CREATE VIEW"]
  on_schema { schema_name="${snowflake_database.analytics.name}.${each.value}" }
}
resource "snowflake_grant_privileges_to_account_role" "transformer_future_tables" {
  for_each=local.prod_schemas; account_role_name=snowflake_account_role.transformer.name; privileges=["SELECT","INSERT","UPDATE","DELETE","TRUNCATE"]
  on_schema_object { future { object_type_plural="TABLES"; in_schema="${snowflake_database.analytics.name}.${each.value}" } }
}
resource "snowflake_grant_privileges_to_account_role" "transformer_future_views" {
  for_each=local.prod_schemas; account_role_name=snowflake_account_role.transformer.name; privileges=["SELECT"]
  on_schema_object { future { object_type_plural="VIEWS"; in_schema="${snowflake_database.analytics.name}.${each.value}" } }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_marts" {
  account_role_name=snowflake_account_role.analyst.name; privileges=["USAGE"]
  on_schema { schema_name="${snowflake_database.analytics.name}.${snowflake_schema.marts.name}" }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_marts_future_tables" {
  account_role_name=snowflake_account_role.analyst.name; privileges=["SELECT"]
  on_schema_object { future { object_type_plural="TABLES"; in_schema="${snowflake_database.analytics.name}.${snowflake_schema.marts.name}" } }
}
resource "snowflake_grant_privileges_to_account_role" "analyst_dev_schema" {
  for_each=local.dev_schemas; account_role_name=snowflake_account_role.analyst.name; privileges=["USAGE","CREATE TABLE","CREATE VIEW"]
  on_schema { schema_name="${snowflake_database.analytics.name}.${each.value}" }
}

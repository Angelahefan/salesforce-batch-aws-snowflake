locals {
  warehouse_sizes = ["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE"]
  prod_schemas = {
    raw = snowflake_schema.raw.name, source = snowflake_schema.source.name,
    intermediate = snowflake_schema.intermediate.name, staging = snowflake_schema.staging.name,
    marts = snowflake_schema.marts.name, snapshots = snowflake_schema.snapshots.name,
    elementary = snowflake_schema.elementary.name
  }
  dev_schemas = { gina = snowflake_schema.dev_gina.name, vicient = snowflake_schema.dev_vicient.name, derek = snowflake_schema.dev_derek.name }
}

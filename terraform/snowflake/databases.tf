resource "snowflake_database" "analytics" { name = var.database_name; comment = "Salesforce CDC analytics database managed by Terraform." }
resource "snowflake_schema" "raw" { database = snowflake_database.analytics.name; name = "RAW" }
resource "snowflake_schema" "source" { database = snowflake_database.analytics.name; name = "SOURCE" }
resource "snowflake_schema" "intermediate" { database = snowflake_database.analytics.name; name = "INTERMEDIATE" }
resource "snowflake_schema" "staging" { database = snowflake_database.analytics.name; name = "STAGING" }
resource "snowflake_schema" "marts" { database = snowflake_database.analytics.name; name = "MARTS" }
resource "snowflake_schema" "snapshots" { database = snowflake_database.analytics.name; name = "SNAPSHOTS" }
resource "snowflake_schema" "elementary" { database = snowflake_database.analytics.name; name = "ELEMENTARY" }
resource "snowflake_schema" "dev_gina" { database = snowflake_database.analytics.name; name = "DEV_GINA" }
resource "snowflake_schema" "dev_vicient" { database = snowflake_database.analytics.name; name = "DEV_VICIENT" }
resource "snowflake_schema" "dev_derek" { database = snowflake_database.analytics.name; name = "DEV_DEREK" }

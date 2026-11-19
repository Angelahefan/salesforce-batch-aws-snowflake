resource "snowflake_masking_policy" "pii_hash" {
  name="PII_HASH_MASK"; database=snowflake_database.analytics.name; schema=snowflake_schema.marts.name
  argument { name="VAL"; type="VARCHAR(16777216)" }
  return_data_type="VARCHAR(16777216)"
  body=<<-EOT
    case
      when is_role_in_session('${snowflake_account_role.admin.name}')
        or is_role_in_session('${snowflake_account_role.transformer.name}') then val
      else sha2(val, 256)
    end
  EOT
  comment="Hashes Salesforce Contact PII for roles other than admin/transformer."
}
resource "snowflake_grant_privileges_to_account_role" "transformer_pii_hash_apply" {
  account_role_name=snowflake_account_role.transformer.name; privileges=["APPLY"]
  on_schema_object { object_type="MASKING POLICY"; object_name="${snowflake_database.analytics.name}.${snowflake_schema.marts.name}.${snowflake_masking_policy.pii_hash.name}" }
}

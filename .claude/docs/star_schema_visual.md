# Salesforce Star Schema
`fct_opportunity` is one row per current Salesforce Opportunity; dimensions are `dim_account`, `dim_contact`, and role-playing `dim_date`. RAW keeps full CDC event history; intermediate models resolve current state.

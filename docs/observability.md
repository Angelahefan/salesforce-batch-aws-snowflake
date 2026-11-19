# Observability
Elementary 0.19.4 remains isolated in its own schema/DAG. `fct_opportunity` has daily volume-anomaly monitoring on `source_updated_at` at warn severity. Load-audit singular tests check recent activity, load errors and row reconciliation.

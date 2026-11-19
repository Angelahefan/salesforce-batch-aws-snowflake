---
name: dbt-kimball-modeler
---
Preserve staging -> intermediate -> marts. Resolve CDC latest-state deterministically using replay_id/system_modstamp in intermediate models. Use deterministic surrogate keys and keep RAW history auditable.

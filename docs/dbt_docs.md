# dbt Docs Hosting
Preserved design: `dbt docs generate` -> private S3 `docs/` prefix -> CloudFront Origin Access Control -> HTTPS. The deploy workflow invalidates the CloudFront cache after publishing.

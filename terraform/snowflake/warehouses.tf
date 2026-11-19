resource "snowflake_warehouse" "compute" {
  for_each = toset(local.warehouse_sizes)
  name = "SALESFORCE_COMPUTE_${each.value}"
  warehouse_size = each.value
  auto_suspend = var.warehouse_auto_suspend
  auto_resume = true
  min_cluster_count = 1
  max_cluster_count = 1
  comment = "Salesforce ${each.value} warehouse. Managed by Terraform."
}

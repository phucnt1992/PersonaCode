resource "azurerm_service_plan" "django" {
  name     = var.name
  location = var.location
  os_type  = "Linux"
  sku_name = ""

  provider = azurerm.application
}

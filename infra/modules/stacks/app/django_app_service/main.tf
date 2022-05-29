

resource "azurerm_linux_web_app" "django" {
  name                = "example"
  resource_group_name = var.location
  location            = azurerm_service_plan.example.location
  service_plan_id     = azurerm_service_plan.example.id

  site_config {}
}

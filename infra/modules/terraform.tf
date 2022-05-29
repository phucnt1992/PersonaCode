terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.4.0",
      configuration_aliases = [
        azurerm.connectivity,
        azurerm.management,
        azurerm.application
      ]
    }
    time = {
      source  = "hashicorp/time"
      version = ">= 0.7.2"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.1.3"
    }
  }
  required_version = ">=1.1.9"
}

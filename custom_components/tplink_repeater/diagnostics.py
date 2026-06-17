"""Diagnostics support module for troubleshooting user environments with new Firmware APIs."""
from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import TPLinkRepeaterConfigEntry
from .const import CONF_PASSWORD

# Maskowane struktury krytyczne w zapisie konfiguracyjnym w pliku .storage
TO_REDACT = [CONF_PASSWORD]

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: TPLinkRepeaterConfigEntry
) -> dict[str, Any]:
    """Compile a sanitized diagnostics structure."""
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "api_retrieved_data": entry.runtime_data.coordinator.data,
    }
"""The TP-Link Repeater integration."""
import logging
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import TPLinkRepeaterCoordinator

_LOGGER = logging.getLogger(__name__)

# Rejestr platform integrujących sprzęt
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

@dataclass
class TPLinkRepeaterRuntimeData:
    """Class to hold strict-typed runtime data for the TP-Link Repeater."""
    coordinator: TPLinkRepeaterCoordinator

# Otypowanie ścisłe (Type alias) gwarantujące poprawne wnioskowanie typów z obiektu runtime_data
type TPLinkRepeaterConfigEntry = ConfigEntry[TPLinkRepeaterRuntimeData]

async def async_setup_entry(hass: HomeAssistant, entry: TPLinkRepeaterConfigEntry) -> bool:
    """Set up TP-Link Repeater from a user-created config entry."""
    
    # Inicjacja koordynatora powiązanego ze wpisem
    coordinator = TPLinkRepeaterCoordinator(hass, entry)

    try:
        # Pusty start koordynatora weryfikujący czy pierwsza próba połączenia przebiegnie pomyślnie
        await coordinator.async_config_entry_first_refresh()
    except Exception as ex:
        _LOGGER.error("Początkowe łączenie ze wzmacniaczem zakończone krytycznym niepowodzeniem: %s", ex)
        raise ConfigEntryNotReady(f"Repeater jest nieosiągalny z poziomu sieci lub zablokował interfejs: {ex}") from ex

    # Przypisanie referencji koordynatora używając najnowszej reguły entry.runtime_data
    entry.runtime_data = TPLinkRepeaterRuntimeData(coordinator=coordinator)

    # Przekazanie zgromadzonej bazy do platform sensorów
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: TPLinkRepeaterConfigEntry) -> bool:
    """Unload a config entry, dismount platforms and release active tasks."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        _LOGGER.debug("Pomyślnie zwolniono moduły oraz stany logiczne dla wzmacniacza sygnału")
    return unload_ok
"""DataUpdateCoordinator for handling robust TP-Link Repeater local polling."""
import logging
from typing import Any

from tplinkrouterc6u import TplinkRouterProvider
from tplinkrouterc6u.common.exception import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_HOST, CONF_PASSWORD, CONF_USERNAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class TPLinkRepeaterCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to orchestrate background fetching data via cryptography API wrapper."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the data updater and API client."""
        self.host = entry.data[CONF_HOST]
        self.password = entry.data[CONF_PASSWORD]
        self.username = entry.data.get(CONF_USERNAME, "admin")

        # Fabryka biblioteki sama definiuje rodzaj zaszyfrowanego logowania do routera
        # Używamy schematu z protokołem HTTP jako bazy, ze względu na rzadkie wsparcie HTTPS na lokalnych sieciach dla repeaterów
        self.client = TplinkRouterProvider.get_client(
            f"http://{self.host}", 
            self.password, 
            self.username, 
            _LOGGER
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.host}",
            update_interval=DEFAULT_SCAN_INTERVAL,
            # Wartość False zapewnia, że sensory zachowają swój stan i nie będą emitować niepotrzebnych akcji,
            # o ile parametry odczytane w porównaniu klasowym (__eq__) nie ulegną dewiacjom z upływem czasu.
            always_update=False
        )

    def _fetch_data_from_api_sync(self) -> dict[str, Any]:
        """Synchronous wrapper encapsulating the logic of session token (stok) and AES decryptions."""
        try:
            # Wzmacniacze zazwyczaj blokują drugi login po weryfikacji hasła,
            # Wymagane jest więc wielokrotne otwieranie i zamykanie tunelu autoryzacyjnego.
            self.client.single_request_mode = False
            
            if self.client.authorize():
                status_obj = self.client.get_status()
                firmware_obj = self.client.get_firmware()
                
                # Niezwykle ważny element prewencyjny. Niezależnie od obróbki - żeton musi wygasnąć.
                self.client.logout()

                return {
                    # Identyfikacja i stan bazowy
                    "macaddr": getattr(status_obj, "lan_macaddr", None),
                    "model": getattr(firmware_obj, "model", "TP-Link Repeater Model"),
                    "hardware_version": getattr(firmware_obj, "hardware_version", "HW Unidentified"),
                    "firmware_version": getattr(firmware_obj, "firmware_version", "FW Unidentified"),
                    
                    # Parametry telemetryczne
                    "cpu_usage": getattr(status_obj, "cpu_usage", None),
                    "mem_usage": getattr(status_obj, "mem_usage", None),
                    "uptime": getattr(status_obj, "wan_ipv4_uptime", None),
                    "clients_total": getattr(status_obj, "clients_total", 0),
                    
                    # Analiza stanu modułów radiowych nadajnika
                    "wifi_2g_enable": getattr(status_obj, "wifi_2g_enable", False),
                    "wifi_5g_enable": getattr(status_obj, "wifi_5g_enable", False),
                }
            else:
                raise Exception("Urządzenie autoryzowało zapytanie negatywnie (niewłaściwe hasło, zablokowany IP, firmware zbyt nowy).")
                
        except ClientError as ex:
            # Opakowywanie hermetyczne wyjątków z warstwy TCP
            raise UpdateFailed(f"Moduł API TP-Link odrzucił komunikację ze zjawiskiem wyjątku: {ex}") from ex
        except Exception as ex:
            # Wszystkie nieoczekiwane przypadki wylatują pod parasolem standardowego komunikatu UpdateFailed koordynatora HA
            raise UpdateFailed(f"Problem w logice parsowania odpowiedzi JSON ze wzmacniacza: {ex}") from ex

    async def _async_update_data(self) -> dict[str, Any]:
        """Asynchronously delegate the blocking API call to the system executor thread."""
        return await self.hass.async_add_executor_job(self._fetch_data_from_api_sync)
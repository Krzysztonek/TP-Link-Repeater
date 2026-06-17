"""Config flow framework orchestrating setup routines for TP-Link Repeater integration."""
import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from tplinkrouterc6u import TplinkRouterProvider

from .const import DOMAIN, CONF_HOST, CONF_PASSWORD, CONF_USERNAME, DEFAULT_USERNAME

_LOGGER = logging.getLogger(__name__)

# Szkielet wizualnego formularza przedstawianego docelowemu użytkownikowi w HA
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): str,
    }
)

class TPLinkRepeaterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow instance routing setup mechanics for TP-Link Repeater."""

    VERSION = 1

    def _execute_api_connection_test(self, host: str, password: str, username: str) -> str:
        """Test API authentication process and forcibly extract LAN MAC address serving as unique_id."""
        client = TplinkRouterProvider.get_client(
            f"http://{host}", 
            password, 
            username, 
            _LOGGER
        )
        if client.authorize():
            status_obj = client.get_status()
            mac_addr = getattr(status_obj, "lan_macaddr", None)
            
            client.logout()
            
            if not mac_addr:
                raise ValueError("Infrastruktura wzmacniacza nie wyeksponowała parametru LAN MAC. Utrata tożsamości.")
            return str(mac_addr)
        else:
            raise ValueError("Kryptografia odrzucona przez kontroler urządzenia.")

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle the initial setup interface presented via UI."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                # Blokujemy pętlę i sprawdzamy obiekty autoryzacji z poziomu warstwy roboczej procesora głównego
                mac_addr = await self.hass.async_add_executor_job(
                    self._execute_api_connection_test, 
                    user_input[CONF_HOST], 
                    user_input[CONF_PASSWORD], 
                    user_input[CONF_USERNAME]
                )

                # Narzucamy systemowi regułę Unique Config Entry w celach zachowania jednoznaczności na podstawie fizycznego adresu kontrolera
                await self.async_set_unique_id(mac_addr)
                self._abort_if_unique_id_configured()

                # Zamknięcie cyklu z sukcesem, zwracamy referencyjny kontener konfiguracji z opisaną zmyślnie etykietą urządzenia
                return self.async_create_entry(title=f"TP-Link Repeater ({user_input[CONF_HOST]})", data=user_input)

            except ValueError as e:
                _LOGGER.error("Porażka strukturalna logiki logowania: %s", e)
                errors["base"] = "invalid_auth"
            except Exception as e:
                _LOGGER.error("Złamanie procesu autoryzacji po sieci TCP/IP: %s", e)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
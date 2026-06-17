"""Constants for the TP-Link Repeater integration."""
from datetime import timedelta

DOMAIN = "tplink_repeater"

CONF_HOST = "host"
CONF_PASSWORD = "password"
CONF_USERNAME = "username"

# Domyślny użytkownik to admin, mimo że na niektórych panelach logowania TP-Link pyta tylko o hasło.
# API wymaga przekazania stringu z nazwą użytkownika do stworzenia soli kryptograficznej.
DEFAULT_USERNAME = "admin"

# Czas między odpytywaniem repeatera.
# Mniejsza wartość zagraża procesorowi MT7621. Minimalne zalecane wartości dla API LuCI.
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
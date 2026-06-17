"""Binary Sensor structures focusing on Boolean states exposed by the repeater hardware."""
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import TPLinkRepeaterConfigEntry
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: TPLinkRepeaterConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Evaluate config objects and instantiate Boolean representations of radio frequency transmitters."""
    coordinator = entry.runtime_data.coordinator
    
    entities = [
        TPLinkRepeaterBinarySensor(coordinator, "wifi_2g_enable", "Przekaźnik Antenowy 2.4GHz"),
        TPLinkRepeaterBinarySensor(coordinator, "wifi_5g_enable", "Przekaźnik Antenowy 5GHz"),
    ]
    async_add_entities(entities)

class TPLinkRepeaterBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Abstraction for Boolean operational metrics."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator, sensor_type: str, name: str):
        """Bind with the data coordinator engine logic."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self._attr_name = f"{coordinator.data.get('model', 'TP-Link Device')} {name}"
        self._attr_unique_id = f"{coordinator.data.get('macaddr')}_{sensor_type}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data.get("macaddr"))},
        }

    @property
    def is_on(self) -> bool:
        """Evaluate raw JSON data returning Boolean value evaluating interface physical status."""
        return bool(self.coordinator.data.get(self.sensor_type, False))
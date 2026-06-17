"""Sensor architecture module rendering telemetry variables from TP-Link Repeater."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE, UnitOfTime

from . import TPLinkRepeaterConfigEntry
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: TPLinkRepeaterConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Setup logic converting config entries to dynamically populated sensor arrays."""
    coordinator = entry.runtime_data.coordinator
    
    sensors = []
    
    # Warunkowe generowanie encji uodparnia logikę na różnice API w starszych modelach firmware'u (zjawisko KeyErrors w tablicach json).
    if coordinator.data.get("cpu_usage") is not None:
        sensors.append(TPLinkRepeaterSensor(
            coordinator, "cpu_usage", "Utylizacja Mocy Obliczeniowej", 
            PERCENTAGE, "mdi:cpu-64-bit", None
        ))
        
    if coordinator.data.get("mem_usage") is not None:
        sensors.append(TPLinkRepeaterSensor(
            coordinator, "mem_usage", "Utylizacja Pamięci Operacyjnej", 
            PERCENTAGE, "mdi:memory", None
        ))
        
    if coordinator.data.get("clients_total") is not None:
        sensors.append(TPLinkRepeaterSensor(
            coordinator, "clients_total", "Zalogowani Klienci", 
            None, "mdi:network-outline", None
        ))
        
    if coordinator.data.get("uptime") is not None:
        sensors.append(TPLinkRepeaterSensor(
            coordinator, "uptime", "Czas Aktywności Wan (Uptime)", 
            UnitOfTime.SECONDS, "mdi:clock-outline", SensorDeviceClass.DURATION
        ))

    async_add_entities(sensors)

class TPLinkRepeaterSensor(CoordinatorEntity, SensorEntity):
    """Abstractor translating dictionary telemetry from Coordinator into SensorEntities."""

    def __init__(self, coordinator, sensor_type: str, name: str, unit: str | None, icon: str, device_class=None):
        """Construct the object definition inside HA core entity framework."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        
        # Generowanie nazwy prezentacyjnej powiązanej strukturalnie z rozpoznanym modelem Repeatera (np. TP-Link RE650 Zalogowani Klienci)
        self._attr_name = f"{coordinator.data.get('model', 'TP-Link Device')} {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        
        if device_class:
            self._attr_device_class = device_class
        
        # Narzucenie klasyfikacji MEASUREMENT determinuje czy silnik będzie gromadził długofalowe statystyki z wartości w celu rysowania wykresów
        if self.sensor_type in ["cpu_usage", "mem_usage", "clients_total"]:
            self._attr_state_class = SensorStateClass.MEASUREMENT

        self._attr_unique_id = f"{coordinator.data.get('macaddr')}_{sensor_type}"
        
        # Połączenie czujnika z ujednoliconą etykietą urządzania z menu Device Registry (dzięki podaniu MAC na starcie w config_flow)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.data.get("macaddr"))},
            "name": coordinator.data.get("model", "TP-Link Range Extender"),
            "manufacturer": "TP-Link",
            "model": coordinator.data.get("model"),
            "sw_version": coordinator.data.get("firmware_version"),
            "hw_version": coordinator.data.get("hardware_version"),
        }

    @property
    def native_value(self):
        """Map the state of the entity extracting numerical constants."""
        val = self.coordinator.data.get(self.sensor_type)
        if val is None:
            return None
            
        # Zjawisko zwracania przez bibliotekę ułamków z przedziału (0.0-1.0) wymaga konwersji arytmetycznej do standardowego procentowego wymiaru (0-100%).
        if self.sensor_type in ["cpu_usage", "mem_usage"]:
            return round(val * 100, 1)
        return val
"""Support for the Colorfulclouds service."""

import logging

from homeassistant.const import ATTR_ATTRIBUTION, ATTR_DEVICE_CLASS, CONF_NAME
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import Entity

from .const import (
    ATTR_ICON,
    ATTR_LABEL,
    ATTRIBUTION,
    COORDINATOR,
    DOMAIN,
    MANUFACTURER,
    OPTIONAL_SENSORS,
    SENSOR_TYPES,
)

PARALLEL_UPDATES = 1
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add Colorfulclouds entities from a config_entry."""
    name = config_entry.data[CONF_NAME]

    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]

    sensors = []
    for sensor in SENSOR_TYPES:
        sensors.append(ColorfulcloudsSensor(name, sensor, coordinator))
    async_add_entities(sensors, False)


class ColorfulcloudsSensor(Entity):
    """Define an Colorfulclouds entity."""

    def __init__(self, name, kind, coordinator, forecast_day=None):
        """Initialize."""
        self._name = name
        self.kind = kind
        self.coordinator = coordinator
        self._device_class = None
        self._attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}
        self._unit_system = (
            "Metric"
            if self.coordinator.data["is_metric"] == "metric:v2"
            else "Imperial"
        )
        self.forecast_day = forecast_day

    @property
    def name(self):
        """Return the name."""
        if self.forecast_day is not None:
            return f"{self._name} {SENSOR_TYPES[self.kind][ATTR_LABEL]} {self.forecast_day}d"
        return f"{self._name} {SENSOR_TYPES[self.kind][ATTR_LABEL]}"

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        # _LOGGER.info("sensor_unique_id: %s", self.coordinator.data["location_key"])
        return f"{self.coordinator.data['location_key']}-{self.kind}".lower()

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data["location_key"])},
            "name": self._name,
            "manufacturer": MANUFACTURER,
            "entry_type": DeviceEntryType.SERVICE,
        }

    @property
    def should_poll(self):
        """Return the polling requirement of the entity."""
        return False

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def state(self):
        """Return the state."""
        try:
            realtime = self.coordinator.data["result"]["realtime"]
            if self.kind == "apparent_temperature":
                return realtime[self.kind]
            if self.kind == "pressure":
                return realtime[self.kind]
            if self.kind == "temperature":
                return realtime[self.kind]
            if self.kind == "humidity":
                return round(float(realtime[self.kind]) * 100)
            if self.kind == "cloudrate":
                return round(float(realtime[self.kind]) * 100)
            if self.kind == "visibility":
                return realtime[self.kind]
            if self.kind == "WindSpeed":
                return realtime["wind"]["speed"]
            if self.kind == "WindDirection":
                return realtime["wind"]["direction"]
            if self.kind == "comfort":
                return realtime["life_index"]["comfort"]["index"]
            if self.kind == "ultraviolet":
                return realtime["life_index"]["ultraviolet"]["index"]
            if self.kind == "precipitation":
                return realtime["precipitation"]["local"]["intensity"]
        except (KeyError, TypeError):
            return None
        return None

    @property
    def icon(self):
        """Return the icon."""
        # if self.forecast_day is not None:
        #     return FORECAST_SENSOR_TYPES[self.kind][ATTR_ICON]
        return SENSOR_TYPES[self.kind][ATTR_ICON]

    @property
    def device_class(self):
        """Return the device_class."""
        # if self.forecast_day is not None:
        #     return FORECAST_SENSOR_TYPES[self.kind][ATTR_DEVICE_CLASS]
        return SENSOR_TYPES[self.kind][ATTR_DEVICE_CLASS]

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        # if self.forecast_day is not None:
        #     return FORECAST_SENSOR_TYPES[self.kind][self._unit_system]
        return SENSOR_TYPES[self.kind][self._unit_system]

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        realtime = self.coordinator.data["result"]["realtime"]
        if self.kind == "ultraviolet":
            self._attrs["desc"] = (
                realtime.get("life_index", {})
                .get("ultraviolet", {})
                .get("desc", "")
            )
        elif self.kind == "comfort":
            self._attrs["desc"] = (
                realtime.get("life_index", {}).get("comfort", {}).get("desc", "")
            )
        elif self.kind == "precipitation":
            precipitation = realtime.get("precipitation", {})
            self._attrs["datasource"] = (
                precipitation.get("local", {}).get("datasource", "")
            )
            self._attrs["nearest_intensity"] = (
                precipitation.get("nearest", {}).get("intensity", "")
            )
            self._attrs["nearest_distance"] = (
                precipitation.get("nearest", {}).get("distance", "")
            )
        return self._attrs

    @property
    def entity_registry_enabled_default(self):
        """Return if the entity should be enabled when first added to the entity registry."""
        return bool(self.kind not in OPTIONAL_SENSORS)

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Colorfulclouds entity."""
        await self.coordinator.async_request_refresh()

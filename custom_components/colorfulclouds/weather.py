from __future__ import annotations

import logging
from homeassistant.components.weather import (
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_CLOUDY,
    ATTR_CONDITION_FOG,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_PARTLYCLOUDY,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_SUNNY,
    ATTR_CONDITION_CLEAR_NIGHT,
    ATTR_CONDITION_WINDY,
    ATTR_CONDITION_POURING,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_HUMIDITY,
    ATTR_WEATHER_CLOUD_COVERAGE,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_VISIBILITY,
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import CONF_NAME
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import ATTRIBUTION, COORDINATOR, DOMAIN, MANUFACTURER

PARALLEL_UPDATES = 1
_LOGGER = logging.getLogger(__name__)

CONDITION_MAP = {
    "CLEAR_DAY": ATTR_CONDITION_SUNNY,
    "CLEAR_NIGHT": ATTR_CONDITION_CLEAR_NIGHT,
    "PARTLY_CLOUDY_DAY": ATTR_CONDITION_PARTLYCLOUDY,
    "PARTLY_CLOUDY_NIGHT": ATTR_CONDITION_PARTLYCLOUDY,
    "CLOUDY": ATTR_CONDITION_CLOUDY,
    "LIGHT_HAZE": ATTR_CONDITION_FOG,
    "MODERATE_HAZE": ATTR_CONDITION_FOG,
    "HEAVY_HAZE": ATTR_CONDITION_FOG,
    "LIGHT_RAIN": ATTR_CONDITION_RAINY,
    "MODERATE_RAIN": ATTR_CONDITION_RAINY,
    "HEAVY_RAIN": ATTR_CONDITION_POURING,
    "STORM_RAIN": ATTR_CONDITION_POURING,
    "FOG": ATTR_CONDITION_FOG,
    "LIGHT_SNOW": ATTR_CONDITION_SNOWY,
    "MODERATE_SNOW": ATTR_CONDITION_SNOWY,
    "HEAVY_SNOW": ATTR_CONDITION_SNOWY,
    "STORM_SNOW": ATTR_CONDITION_SNOWY,
    "DUST": ATTR_CONDITION_FOG,
    "SAND": ATTR_CONDITION_FOG,
    "THUNDER_SHOWER": ATTR_CONDITION_LIGHTNING_RAINY,
    "HAIL": ATTR_CONDITION_HAIL,
    "SLEET": ATTR_CONDITION_SNOWY_RAINY,
    "WIND": ATTR_CONDITION_WINDY,
    "HAZE": ATTR_CONDITION_FOG,
    "RAIN": ATTR_CONDITION_RAINY,
    "SNOW": ATTR_CONDITION_SNOWY,
    "FREEZE": ATTR_CONDITION_SNOWY_RAINY,
    "BLOWING_SAND": ATTR_CONDITION_WINDY,
}


def _get_condition(skycon: str, default: str | None = None) -> str | None:
    """Map a Colorfulclouds skycon to a Home Assistant weather condition."""
    return CONDITION_MAP.get(skycon, default)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add a Colorfulclouds weather entity from a config_entry."""
    name = config_entry.data[CONF_NAME]

    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    # _LOGGER.debug("metric: %s", coordinator.data["is_metric"])

    async_add_entities([ColorfulCloudsEntity(name, coordinator)], True)


class ColorfulCloudsEntity(WeatherEntity):
    """Representation of a weather condition."""

    _attr_supported_features = (
        WeatherEntityFeature.FORECAST_HOURLY | WeatherEntityFeature.FORECAST_DAILY
    )

    def __init__(self, name, coordinator):
        self.coordinator = coordinator
        _LOGGER.debug("coordinator: %s", coordinator.data["server_time"])
        self._name = name
        self._attrs = {}

    @property
    def name(self):
        return self._name

    @property
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        _LOGGER.debug("weather_unique_id: %s", self.coordinator.data["location_key"])
        return self.coordinator.data["location_key"]

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
        """Return the weather condition."""
        skycon = self.coordinator.data["result"]["realtime"]["skycon"]
        return _get_condition(skycon)

    @property
    def cloud_coverage(self):
        return round(
            float(self.coordinator.data["result"]["realtime"]["cloudrate"]) * 100
        )

    @property
    def condition(self):
        """Return the weather condition."""
        skycon = self.coordinator.data["result"]["realtime"]["skycon"]
        return _get_condition(skycon)

    @property
    def humidity(self):
        return round(float(self.coordinator.data["result"]["realtime"]["humidity"]) * 100)

    @property
    def native_apparent_temperature(self):
        return self.coordinator.data["result"]["realtime"]["apparent_temperature"]

    @property
    def native_precipitation_unit(self):
        return "mm" if self.coordinator.data["is_metric"] == "metric:v2" else "in"

    @property
    def native_pressure(self):
        return self.coordinator.data["result"]["realtime"]["pressure"]

    @property
    def native_pressure_unit(self):
        return "Pa"

    @property
    def native_temperature(self):
        return self.coordinator.data["result"]["realtime"]["temperature"]

    @property
    def native_temperature_unit(self):
        return "°C" if self.coordinator.data["is_metric"] == "metric:v2" else "°F"

    @property
    def native_visibility(self):
        """能见度"""
        return self.coordinator.data["result"]["realtime"]["visibility"]

    @property
    def native_visibility_unit(self):
        return "km" if self.coordinator.data["is_metric"] == "metric:v2" else "mi"

    @property
    def native_wind_speed(self):
        """风速"""
        return self.coordinator.data["result"]["realtime"]["wind"]["speed"]

    @property
    def wind_bearing(self):
        """风向"""
        return self.coordinator.data["result"]["realtime"]["wind"]["direction"]

    @property
    def native_wind_speed_unit(self):
        return "km/h" if self.coordinator.data["is_metric"] == "metric:v2" else "mph"

    @property
    def uv_index(self):
        """紫外线"""
        return self.coordinator.data["result"]["realtime"]["life_index"]["ultraviolet"][
            "index"
        ]

    @property
    def extra_state_attributes(self):
        result = self.coordinator.data["result"]
        realtime = result["realtime"]
        minutely = result.get("minutely", {})
        air_quality = realtime.get("air_quality", {})
        aqi = air_quality.get("aqi", {})
        aqi_description = air_quality.get("description", {})

        self._attrs = {
            "skycon": realtime["skycon"],
            "forecast_hourly": result.get("hourly", {}).get("description", ""),
            "forecast_minutely": minutely.get("description", ""),
            "forecast_probability": minutely.get("probability", ""),
            "forecast_keypoint": result.get("forecast_keypoint", ""),
            "forecast_alert": result.get("alert", ""),
            "pm25": air_quality.get("pm25", ""),
            "pm10": air_quality.get("pm10", ""),
            "o3": air_quality.get("o3", ""),
            "no2": air_quality.get("no2", ""),
            "so2": air_quality.get("so2", ""),
            "co": air_quality.get("co", ""),
            "aqi": aqi.get("chn", ""),
            "aqi_description": aqi_description.get("chn", ""),
            "aqi_usa": aqi.get("usa", ""),
            "aqi_usa_description": aqi_description.get("usa", ""),
        }
        return self._attrs

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Colorfulclouds entity."""
        await self.coordinator.async_request_refresh()

    async def async_forecast_daily(self) -> list[Forecast] | None:
        daily = self.coordinator.data["result"]["daily"]
        forecast_data = []
        try:
            for i in range(len(daily["temperature"])):
                skycon = daily["skycon"][i]["value"]
                forecast_data.append(
                    {
                        ATTR_FORECAST_TIME: daily["temperature"][i]["date"],
                        "skycon": skycon,
                        ATTR_FORECAST_CONDITION: _get_condition(
                            skycon, ATTR_CONDITION_CLOUDY
                        ),
                        ATTR_FORECAST_NATIVE_TEMP: daily["temperature"][i]["max"],
                        ATTR_FORECAST_NATIVE_TEMP_LOW: daily["temperature"][i][
                            "min"
                        ],
                        ATTR_FORECAST_WIND_BEARING: daily["wind"][i]["avg"][
                            "direction"
                        ],
                        ATTR_FORECAST_NATIVE_WIND_SPEED: daily["wind"][i]["avg"][
                            "speed"
                        ],
                        ATTR_FORECAST_PRECIPITATION: daily["precipitation"][i][
                            "avg"
                        ],
                        ATTR_FORECAST_HUMIDITY: round(
                            float(daily["humidity"][i]["avg"]) * 100
                        ),
                        ATTR_WEATHER_CLOUD_COVERAGE: round(
                            float(daily["cloudrate"][i]["avg"]) * 100
                        ),
                        ATTR_WEATHER_PRESSURE: daily["pressure"][i]["avg"],
                        ATTR_WEATHER_VISIBILITY: daily["visibility"][i]["avg"],
                    }
                )
        except (KeyError, IndexError, TypeError) as error:
            _LOGGER.warning("Unable to build daily forecast: %s", error)

        return forecast_data

    async def async_forecast_hourly(self) -> list[Forecast] | None:
        hourly = self.coordinator.data["result"]["hourly"]
        forecast_data = []
        try:
            for i in range(len(hourly["temperature"])):
                skycon = hourly["skycon"][i]["value"]
                forecast_data.append(
                    {
                        ATTR_FORECAST_TIME: hourly["temperature"][i]["datetime"],
                        "skycon": skycon,
                        ATTR_FORECAST_CONDITION: _get_condition(
                            skycon, ATTR_CONDITION_CLOUDY
                        ),
                        ATTR_FORECAST_NATIVE_TEMP: hourly["temperature"][i][
                            "value"
                        ],
                        ATTR_FORECAST_WIND_BEARING: hourly["wind"][i]["direction"],
                        ATTR_FORECAST_NATIVE_WIND_SPEED: hourly["wind"][i]["speed"],
                        ATTR_FORECAST_PRECIPITATION: hourly["precipitation"][i][
                            "value"
                        ],
                        ATTR_WEATHER_HUMIDITY: round(
                            float(hourly["humidity"][i]["value"]) * 100
                        ),
                        ATTR_WEATHER_CLOUD_COVERAGE: round(
                            float(hourly["cloudrate"][i]["value"]) * 100
                        ),
                        ATTR_WEATHER_PRESSURE: hourly["pressure"][i]["value"],
                        ATTR_WEATHER_VISIBILITY: hourly["visibility"][i]["value"],
                    }
                )
        except (KeyError, IndexError, TypeError) as error:
            _LOGGER.warning("Unable to build hourly forecast: %s", error)

        return forecast_data

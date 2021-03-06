

"""Constants for colorfulclouds."""
DOMAIN = "colorfulclouds"

PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    "const.py",
    "manifest.json",
    "weather.py",
    "config_flow.py",
    "services.yaml",
    "translations/en.json",
]
VERSION = "0.1.3"
ISSUE_URL = "https://github.com/fineemb/Colorfulclouds-weather/issues"

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    DEVICE_CLASS_TEMPERATURE,
    LENGTH_FEET,
    LENGTH_INCHES,
    LENGTH_METERS,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    LENGTH_MILES,
    LENGTH_KILOMETERS,
    LENGTH_INCHES,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    TIME_HOURS,
    DEGREE,
    UV_INDEX,
    VOLUME_CUBIC_METERS,
)

ATTRIBUTION = "Data provided by Colorfulclouds"
ATTR_ICON = "icon"
ATTR_FORECAST = CONF_DAILYSTEPS = "forecast"
ATTR_LABEL = "label"
ATTR_UNIT_IMPERIAL = "Imperial"
ATTR_UNIT_METRIC = "Metric"
MANUFACTURER = "Colorfulclouds, Inc."
NAME = "Colorfulclouds"

CONF_API_KEY = "api_key"
CONF_API_VERSION = "api_version"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_ALERT = "alert"
CONF_HOURLYSTEPS = "hourlysteps"
CONF_DAILYSTEPS = "dailysteps"
CONF_STARTTIME = "starttime"

COORDINATOR = "coordinator"

UNDO_UPDATE_LISTENER = "undo_update_listener"


OPTIONAL_SENSORS = (

    "WindDirection",
)


SENSOR_TYPES = {
    "apparent_temperature": {
        ATTR_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        ATTR_ICON: None,
        ATTR_LABEL: "感觉温度",
        ATTR_UNIT_METRIC: TEMP_CELSIUS,
        ATTR_UNIT_IMPERIAL: TEMP_FAHRENHEIT,
    },
    "temperature": {
        ATTR_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        ATTR_ICON: None,
        ATTR_LABEL: "温度",
        ATTR_UNIT_METRIC: TEMP_CELSIUS,
        ATTR_UNIT_IMPERIAL: TEMP_FAHRENHEIT,
    },
    "cloudrate": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-cloudy",
        ATTR_LABEL: "云量",
        ATTR_UNIT_METRIC: "%",
        ATTR_UNIT_IMPERIAL: "%",
    },
    "precipitation": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-rainy",
        ATTR_LABEL: "雨量",
        ATTR_UNIT_METRIC: "mm",
        ATTR_UNIT_IMPERIAL: LENGTH_INCHES,
    },
    "pressure": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:gauge",
        ATTR_LABEL: "气压",
        ATTR_UNIT_METRIC: "Pa",
        ATTR_UNIT_IMPERIAL: "Pa",
    },
    "comfort": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:gauge",
        ATTR_LABEL: "舒适指数",
        ATTR_UNIT_METRIC: None,
        ATTR_UNIT_IMPERIAL: None,
    },
    "ultraviolet": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-sunny",
        ATTR_LABEL: "紫外线",
        ATTR_UNIT_METRIC: UV_INDEX,
        ATTR_UNIT_IMPERIAL: UV_INDEX,
    },
    "humidity": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:water-percent",
        ATTR_LABEL: "湿度",
        ATTR_UNIT_METRIC: "%",
        ATTR_UNIT_IMPERIAL: "%",
    },
    "visibility": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-fog",
        ATTR_LABEL: "能见度",
        ATTR_UNIT_METRIC: LENGTH_KILOMETERS,
        ATTR_UNIT_IMPERIAL: LENGTH_MILES,
    },
    "WindSpeed": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-windy",
        ATTR_LABEL: "风速",
        ATTR_UNIT_METRIC: SPEED_KILOMETERS_PER_HOUR,
        ATTR_UNIT_IMPERIAL: SPEED_MILES_PER_HOUR,
    },
    "WindDirection": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-windy",
        ATTR_LABEL: "风向",
        ATTR_UNIT_METRIC: DEGREE,
        ATTR_UNIT_IMPERIAL: DEGREE,
    },
}




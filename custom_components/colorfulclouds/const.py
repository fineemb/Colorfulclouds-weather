"""Constants for the colorfulClouds integration."""

DOMAIN = "colorfulclouds"

CONF_ALERT = "alert"
CONF_HOURLYSTEPS = "hourlysteps"
CONF_DAILYSTEPS = "dailysteps"
CONF_STARTTIME = "starttime"

COORDINATOR = "coordinator"

UNDO_UPDATE_LISTENER = "undo_update_listener"

ATTRIBUTION = "Data provided by Colorfulclouds"
ATTR_ICON = "icon"
ATTR_FORECAST = CONF_DAILYSTEPS = "forecast"
ATTR_LABEL = "label"
ATTR_UNIT_IMPERIAL = "Imperial"
ATTR_UNIT_METRIC = "Metric"
MANUFACTURER = "Colorfulclouds, Inc."
NAME = "Colorfulclouds"

from homeassistant.const import ATTR_DEVICE_CLASS, DEGREE, UV_INDEX

OPTIONAL_SENSORS = ()
SENSOR_TYPES = {
    "apparent_temperature": {
        ATTR_DEVICE_CLASS: "temperature",
        ATTR_ICON: None,
        ATTR_LABEL: "感觉温度",
        ATTR_UNIT_METRIC: "°C",
        ATTR_UNIT_IMPERIAL: "°F",
    },
    "temperature": {
        ATTR_DEVICE_CLASS: "temperature",
        ATTR_ICON: None,
        ATTR_LABEL: "温度",
        ATTR_UNIT_METRIC: "°C",
        ATTR_UNIT_IMPERIAL: "°F",
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
        ATTR_UNIT_IMPERIAL: "in",
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
        ATTR_UNIT_METRIC: "km",
        ATTR_UNIT_IMPERIAL: "mi",
    },
    "WindSpeed": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:weather-windy",
        ATTR_LABEL: "风速",
        ATTR_UNIT_METRIC: "km/h",
        ATTR_UNIT_IMPERIAL: "mph",
    },
    "WindDirection": {
        ATTR_DEVICE_CLASS: None,
        ATTR_ICON: "mdi:windsock",
        ATTR_LABEL: "风向",
        ATTR_UNIT_METRIC: DEGREE,
        ATTR_UNIT_IMPERIAL: DEGREE,
    },
}

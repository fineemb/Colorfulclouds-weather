'''
Author        : fineemb
Github        : https://github.com/fineemb
Description   : 
Date          : 2020-06-07 16:40:38
LastEditors   : fineemb
LastEditTime  : 2020-09-12 20:07:33
'''
"""
Component to integrate with 彩云天气.

For more details about this component, please refer to
https://github.com/fineemb/Colorfulclouds-weather
"""
import asyncio
import requests
import json
import datetime
import logging

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout

from homeassistant.const import CONF_API_KEY
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.unit_system import METRIC_SYSTEM

from .const import (
    ATTR_FORECAST,
    CONF_DAILYSTEPS,
    CONF_HOURLYSTEPS,
    CONF_ALERT,
    CONF_API_VERSION,
    CONF_LONGITUDE,
    CONF_LATITUDE,
    CONF_STARTTIME,
    COORDINATOR,
    DOMAIN,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "weather"]

async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up configured Colorfulclouds."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, config_entry) -> bool:
    """Set up Colorfulclouds as config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    location_key = config_entry.unique_id
    longitude = config_entry.data[CONF_LONGITUDE]
    latitude = config_entry.data[CONF_LATITUDE]
    api_version = config_entry.data[CONF_API_VERSION]
    dailysteps = config_entry.options.get(CONF_DAILYSTEPS, 5)
    hourlysteps = config_entry.options.get(CONF_HOURLYSTEPS, 24)
    alert = config_entry.options.get(CONF_ALERT, True)
    starttime = config_entry.options.get(CONF_STARTTIME, 0)

    _LOGGER.debug("Using location_key: %s, get forecast: %s", location_key, api_version)

    websession = async_get_clientsession(hass)

    coordinator = ColorfulcloudsDataUpdateCoordinator(
        hass, websession, api_key, api_version, location_key, longitude, latitude, dailysteps, hourlysteps, alert, starttime
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    undo_listener = config_entry.add_update_listener(update_listener)

    hass.data[DOMAIN][config_entry.entry_id] = {
        COORDINATOR: coordinator,
        UNDO_UPDATE_LISTENER: undo_listener,
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(config_entry, component)
        )

    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(config_entry, component)
                for component in PLATFORMS
            ]
        )
    )

    hass.data[DOMAIN][config_entry.entry_id][UNDO_UPDATE_LISTENER]()

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Update listener."""
    await hass.config_entries.async_reload(config_entry.entry_id)


class ColorfulcloudsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Colorfulclouds data API."""

    def __init__(self, hass, session, api_key, api_version, location_key, longitude, latitude, dailysteps: int, hourlysteps: int, alert: bool, starttime: int):
        """Initialize."""
        self.location_key = location_key
        self.longitude = longitude
        self.latitude = latitude
        self.dailysteps = dailysteps
        self.alert = alert
        self.hourlysteps = hourlysteps
        self.api_version = api_version
        self.api_key = api_key
        self.starttime = starttime
        self.is_metric = "metric:v2"
        if hass.config.units is METRIC_SYSTEM:
            self.is_metric = "metric:v2"
        else:
            self.is_metric = "imperial"

        update_interval = (
            datetime.timedelta(minutes=6)
        )
        _LOGGER.debug("Data will be update every %s", update_interval)

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    # @asyncio.coroutine
    def get_data(self, url):
        json_text = requests.get(url).content
        resdata = json.loads(json_text)
        return resdata

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with timeout(10):
                start_timestamp = int((datetime.datetime.now()+datetime.timedelta(days=self.starttime)).timestamp())
                url = str.format("https://api.caiyunapp.com/{}/{}/{},{}/weather.json?dailysteps={}&hourlysteps={}&alert={}&unit={}&timestamp={}", self.api_version, self.api_key, self.longitude, self.latitude, self.dailysteps, self.hourlysteps, self.alert, self.is_metric, start_timestamp)
                # json_text = requests.get(url).content
                resdata =  await self.hass.async_add_executor_job(self.get_data, url)
        except (
            ClientConnectorError
        ) as error:
            raise UpdateFailed(error)
        _LOGGER.debug("Requests remaining: %s", url)
        return {**resdata,"location_key":self.location_key,"is_metric":self.is_metric}



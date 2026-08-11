"""The Colorfulclouds integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_API_VERSION,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_ALERT,
    CONF_DAILYSTEPS,
    CONF_HOURLYSTEPS,
    CONF_STARTTIME,
    CONF_INTERVAL,
    COORDINATOR,
    DOMAIN,
    UNDO_UPDATE_LISTENER,
)

from .colorfulclouds import ColorfulcloudsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.WEATHER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Colorfulclouds as config entry."""
    hass.data.setdefault(DOMAIN, {})
    api_key = config_entry.data[CONF_API_KEY]
    location_key = config_entry.unique_id
    longitude = config_entry.data[CONF_LONGITUDE]
    latitude = config_entry.data[CONF_LATITUDE]
    api_version = config_entry.data[CONF_API_VERSION]
    dailysteps = config_entry.options.get(CONF_DAILYSTEPS, 5)
    hourlysteps = config_entry.options.get(CONF_HOURLYSTEPS, 24)
    alert = config_entry.options.get(CONF_ALERT, True)
    starttime = config_entry.options.get(CONF_STARTTIME, 0)
    interval = config_entry.options.get(CONF_INTERVAL, 10)
    websession = async_get_clientsession(hass)
    coordinator = ColorfulcloudsDataUpdateCoordinator(
        hass,
        websession,
        api_key,
        api_version,
        location_key,
        longitude,
        latitude,
        dailysteps,
        hourlysteps,
        alert,
        starttime,
        interval,
    )
    await coordinator.async_config_entry_first_refresh()
    undo_listener = config_entry.add_update_listener(update_listener)
    hass.data[DOMAIN][config_entry.entry_id] = {
        COORDINATOR: coordinator,
        UNDO_UPDATE_LISTENER: undo_listener,
    }
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    if unload_ok:
        entry_data = hass.data[DOMAIN].pop(config_entry.entry_id)
        entry_data[UNDO_UPDATE_LISTENER]()

    return unload_ok


async def update_listener(hass, config_entry):
    """Update listener."""
    await hass.config_entries.async_reload(config_entry.entry_id)

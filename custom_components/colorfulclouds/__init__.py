"""The colorfulClouds integration."""

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

from .const import (
    CONF_ALERT,
    CONF_DAILYSTEPS,
    CONF_HOURLYSTEPS,
    CONF_STARTTIME,
    COORDINATOR,
    DOMAIN,
    UNDO_UPDATE_LISTENER,
)

_LOGGER = logging.getLogger(__name__)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .colorfulclouds import ColorfulcloudsDataUpdateCoordinator

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.WEATHER, Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
# type ColorfulClouds_ConfigEntry = ConfigEntry[MyApi]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
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
    # _LOGGER.debug("Using location_key: %s, get forecast: %s", location_key, api_version)
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
    hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload_ok


async def update_listener(hass, config_entry):
    """Update listener."""
    await hass.config_entries.async_reload(config_entry.entry_id)

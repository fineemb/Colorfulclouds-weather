"""Config flow for the Colorfulclouds integration."""

from __future__ import annotations

from collections import OrderedDict
import json
import logging

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_NAME,
)
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_ALERT,
    CONF_DAILYSTEPS,
    CONF_HOURLYSTEPS,
    CONF_STARTTIME,
    CONF_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class ColorfulcloudsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Colorfulclouds."""

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ColorfulcloudsOptionsFlow()

    def __init__(self):
        """Initialize."""
        self._errors = {}

    def get_data(self, url):
        """Fetch and parse JSON from the given URL."""
        json_text = requests.get(url, timeout=10).content
        return json.loads(json_text)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        self._errors = {}
        if user_input is None:
            return await self._show_config_form(user_input)

        # Check if the location is already configured.
        existing = await self._check_existing(user_input[CONF_NAME])
        if existing:
            return self.async_abort(reason="already_configured")

        # Test the API credentials.
        url = (
            f"https://api.caiyunapp.com/{user_input['api_version']}/"
            f"{user_input['api_key']}/{user_input['longitude']},"
            f"{user_input['latitude']}/daily.json"
        )
        try:
            redata = await self.hass.async_add_executor_job(self.get_data, url)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as error:
            _LOGGER.warning("Unable to connect to Colorfulclouds API: %s", error)
            self._errors["base"] = "cannot_connect"
            return await self._show_config_form(user_input)

        if redata.get("status") != "ok":
            self._errors["base"] = "communication"
            return await self._show_config_form(user_input)

        await self.async_set_unique_id(
            f"{user_input['longitude']}-{user_input['latitude']}".replace(".", "_")
        )
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to the user."""
        # Defaults
        api_version = "v2.5"
        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_API_KEY)] = str
        data_schema[vol.Optional("api_version", default=api_version)] = str
        data_schema[
            vol.Optional(CONF_LONGITUDE, default=self.hass.config.longitude)
        ] = cv.longitude
        data_schema[vol.Optional(CONF_LATITUDE, default=self.hass.config.latitude)] = (
            cv.latitude
        )
        data_schema[vol.Optional(CONF_NAME, default=self.hass.config.location_name)] = (
            str
        )
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=self._errors
        )

    async def _check_existing(self, host):
        for entry in self._async_current_entries():
            if host == entry.data.get(CONF_NAME):
                return True
        return False


class ColorfulcloudsOptionsFlow(config_entries.OptionsFlow):
    """Config flow options for Colorfulclouds."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_DAILYSTEPS,
                        default=self.config_entry.options.get(CONF_DAILYSTEPS, 5),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5, max=15)),
                    vol.Optional(
                        CONF_INTERVAL,
                        default=self.config_entry.options.get(CONF_INTERVAL, 10),
                    ): vol.All(vol.Coerce(int), vol.Range(min=5)),
                    vol.Optional(
                        CONF_HOURLYSTEPS,
                        default=self.config_entry.options.get(CONF_HOURLYSTEPS, 24),
                    ): vol.All(vol.Coerce(int), vol.Range(min=24, max=360)),
                    vol.Optional(
                        CONF_STARTTIME,
                        default=self.config_entry.options.get(CONF_STARTTIME, 0),
                    ): vol.All(vol.Coerce(int), vol.Range(min=-5, max=0)),
                    vol.Optional(
                        CONF_ALERT,
                        default=self.config_entry.options.get(CONF_ALERT, True),
                    ): bool,
                }
            ),
        )

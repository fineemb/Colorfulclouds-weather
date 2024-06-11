"""Config flow for colorfulClouds integration."""

from __future__ import annotations

from collections import OrderedDict
import json
import logging

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
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

# TODO adjust the data schema to the data that you need
# STEP_USER_DATA_SCHEMA = vol.Schema(
#     {
#         vol.Required(CONF_API_KEY): str,
#         vol.Required(CONF_LATITUDE): str,
#         vol.Required(CONF_LONGITUDE): str,
#         vol.Required(CONF_API_VERSION): str,
#     }
# )


@config_entries.HANDLERS.register(DOMAIN)
class ColorfulcloudslowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ColorfulcloudsOptionsFlow(config_entry)

    def __init__(self):
        """Initialize."""
        self._errors = {}

    # @asyncio.coroutine
    def get_data(self, url):
        json_text = requests.get(url).content
        resdata = json.loads(json_text)
        return resdata

    async def async_step_user(self, user_input={}):
        self._errors = {}
        if user_input is not None:
            # Check if entered host is already in HomeAssistant
            existing = await self._check_existing(user_input[CONF_NAME])
            if existing:
                return self.async_abort(reason="already_configured")

            # If it is not, continue with communication test
            url = str.format(
                "https://api.caiyunapp.com/{}/{}/{},{}/daily.json",
                user_input["api_version"],
                user_input["api_key"],
                user_input["longitude"],
                user_input["latitude"],
            )
            redata = await self.hass.async_add_executor_job(self.get_data, url)
            status = redata["status"]
            if status == "ok":
                await self.async_set_unique_id(
                    f"{user_input['longitude']}-{user_input['latitude']}".replace(
                        ".", "_"
                    )
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )
            else:
                self._errors["base"] = "communication"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
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

    async def async_step_import(self, user_input):
        """Import a config entry.

        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

    async def _check_existing(self, host):
        for entry in self._async_current_entries():
            if host == entry.data.get(CONF_NAME):
                return True


class ColorfulcloudsOptionsFlow(config_entries.OptionsFlow):
    """Config flow options for Colorfulclouds."""

    def __init__(self, config_entry):
        """Initialize Colorfulclouds options flow."""
        self.config_entry = config_entry

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
                        default=self.config_entry.options.get(CONF_INTERVAL, 5),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1)),
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


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

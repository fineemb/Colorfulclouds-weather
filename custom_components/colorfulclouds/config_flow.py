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
    CONF_API_VERSION,
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


def _fetch_api_data(url):
    """Fetch and parse JSON from the given URL."""
    json_text = requests.get(url, timeout=10).content
    return json.loads(json_text)


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
            f"https://api.caiyunapp.com/{user_input[CONF_API_VERSION]}/"
            f"{user_input[CONF_API_KEY]}/{user_input['longitude']},"
            f"{user_input['latitude']}/daily.json"
        )
        try:
            redata = await self.hass.async_add_executor_job(_fetch_api_data, url)
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
        data_schema[vol.Optional(CONF_API_VERSION, default=api_version)] = str
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

    def __init__(self):
        """Initialize."""
        self._errors = {}

    @property
    def _api_key(self):
        """Return the configured API key, options take precedence."""
        return self.config_entry.options.get(
            CONF_API_KEY
        ) or self.config_entry.data.get(CONF_API_KEY, "")

    @property
    def _api_version(self):
        """Return the configured API version, options take precedence."""
        return self.config_entry.options.get(
            CONF_API_VERSION
        ) or self.config_entry.data.get(CONF_API_VERSION, "v2.5")

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}
        if user_input is not None:
            # Test the API credentials before saving.
            api_key = user_input.get(CONF_API_KEY) or self._api_key
            api_version = user_input.get(CONF_API_VERSION) or self._api_version
            url = (
                f"https://api.caiyunapp.com/{api_version}/{api_key}/"
                f"{self.config_entry.data[CONF_LONGITUDE]},"
                f"{self.config_entry.data[CONF_LATITUDE]}/daily.json"
            )
            try:
                redata = await self.hass.async_add_executor_job(_fetch_api_data, url)
            except (requests.exceptions.RequestException, json.JSONDecodeError) as error:
                _LOGGER.warning("Unable to connect to Colorfulclouds API: %s", error)
                self._errors["base"] = "cannot_connect"
                return await self._show_options_form(user_input)

            if redata.get("status") != "ok":
                self._errors["base"] = "communication"
                return await self._show_options_form(user_input)

            return self.async_create_entry(title="", data=user_input)

        return await self._show_options_form(user_input)

    async def _show_options_form(self, user_input):
        """Show the options form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_API_KEY, default=self._api_key): str,
                    vol.Optional(
                        CONF_API_VERSION, default=self._api_version
                    ): str,
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
            errors=self._errors,
        )

"""Data update coordinator for the Colorfulclouds integration."""

import asyncio
import datetime
import logging

from aiohttp import ClientError
from async_timeout import timeout

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.unit_system import METRIC_SYSTEM

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ColorfulcloudsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Colorfulclouds data API."""

    def __init__(
        self,
        hass,
        websession,
        api_key,
        api_version,
        location_key,
        longitude,
        latitude,
        dailysteps: int,
        hourlysteps: int,
        alert: bool,
        starttime: int,
        interval: int,
    ):
        """Initialize."""
        self.location_key = location_key
        self.longitude = longitude
        self.latitude = latitude
        self.dailysteps = dailysteps
        self.alert = alert
        self.interval = interval
        self.hourlysteps = hourlysteps
        self.api_version = api_version
        self.api_key = api_key
        self.starttime = starttime
        self.websession = websession
        self.is_metric = "metric:v2" if hass.config.units is METRIC_SYSTEM else "imperial"

        update_interval = datetime.timedelta(minutes=self.interval)
        _LOGGER.debug("Data will be updated every %s", update_interval)

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    def _build_url(self, start_timestamp: int) -> str:
        """Build the Colorfulclouds API URL."""
        return (
            f"https://api.caiyunapp.com/{self.api_version}/{self.api_key}/"
            f"{self.longitude},{self.latitude}/weather.json"
            f"?dailysteps={self.dailysteps}&hourlysteps={self.hourlysteps}"
            f"&alert={str(self.alert).lower()}&unit={self.is_metric}"
            f"&timestamp={start_timestamp}"
        )

    async def _async_update_data(self):
        """Update data via the Colorfulclouds API."""
        start_timestamp = int(
            (
                datetime.datetime.now() + datetime.timedelta(days=self.starttime)
            ).timestamp()
        )
        url = self._build_url(start_timestamp)
        try:
            async with timeout(10):
                resp = await self.websession.get(url)
                resdata = await resp.json()
        except (ClientError, asyncio.TimeoutError) as error:
            raise UpdateFailed(
                f"Error communicating with Colorfulclouds API: {error}"
            ) from error
        except ValueError as error:
            raise UpdateFailed(
                f"Invalid response from Colorfulclouds API: {error}"
            ) from error

        if resdata.get("status") != "ok":
            raise UpdateFailed(
                "Colorfulclouds API returned an error: "
                f"{resdata.get('error') or resdata.get('status')}"
            )

        _LOGGER.debug("Colorfulclouds data refreshed successfully")
        return {
            **resdata,
            "location_key": self.location_key,
            "is_metric": self.is_metric,
        }

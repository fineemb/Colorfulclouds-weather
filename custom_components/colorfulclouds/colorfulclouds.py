import datetime
import json
import logging

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
import requests

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.unit_system import METRIC_SYSTEM

_LOGGER = logging.getLogger(__name__)
from .const import DOMAIN


class ColorfulcloudsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Colorfulclouds data API."""

    def __init__(
        self,
        hass,
        session,
        api_key,
        api_version,
        location_key,
        longitude,
        latitude,
        dailysteps: int,
        hourlysteps: int,
        alert: bool,
        starttime: int,
    ):
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

        update_interval = datetime.timedelta(minutes=6)
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
                start_timestamp = int(
                    (
                        datetime.datetime.now()
                        + datetime.timedelta(days=self.starttime)
                    ).timestamp()
                )
                url = str.format(
                    "https://api.caiyunapp.com/{}/{}/{},{}/weather.json?dailysteps={}&hourlysteps={}&alert={}&unit={}&timestamp={}",
                    self.api_version,
                    self.api_key,
                    self.longitude,
                    self.latitude,
                    self.dailysteps,
                    self.hourlysteps,
                    str(self.alert).lower(),
                    self.is_metric,
                    start_timestamp,
                )
                # json_text = requests.get(url).content
                resdata = await self.hass.async_add_executor_job(self.get_data, url)
        except ClientConnectorError as error:
            raise UpdateFailed(error)
        _LOGGER.debug("Requests remaining: %s", url)
        return {
            **resdata,
            "location_key": self.location_key,
            "is_metric": self.is_metric,
        }

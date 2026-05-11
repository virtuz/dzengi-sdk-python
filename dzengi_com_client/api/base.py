import json
import logging
import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from ..exceptions import DzengiAPIException, DzengiRequestException


class BaseAPI:
    _REDACTED_FIELDS = {"signature", "api_key", "api_secret", "x-mbx-apikey"}

    def __init__(self, api_key, api_secret, base_url, session, recv_window=5000, logger=None, debug: bool = False):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url
        self._session = session
        self._recv_window = recv_window
        self._time_offset = 0
        self._logger = logger
        self._debug = debug

    def _should_log_debug(self):
        return self._debug and self._logger and self._logger.isEnabledFor(logging.DEBUG)

    def _sanitize_for_logging(self, payload):
        if isinstance(payload, dict):
            return {
                key: "<redacted>" if key.lower() in self._REDACTED_FIELDS else self._sanitize_for_logging(value)
                for key, value in payload.items()
            }
        if isinstance(payload, list):
            return [self._sanitize_for_logging(value) for value in payload]
        return payload

    def _format_for_logging(self, payload):
        if payload is None:
            return "null"
        return json.dumps(self._sanitize_for_logging(payload), sort_keys=True, default=str)

    def _log_request(self, method: str, url: str, params: dict, data: dict, attempt: int):
        if not self._should_log_debug():
            return

        self._logger.debug(
            "Request: %s %s attempt=%s params=%s data=%s",
            method,
            url,
            attempt + 1,
            self._format_for_logging(params),
            self._format_for_logging(data),
        )

    def _log_response(self, method: str, url: str, response: requests.Response):
        if not self._should_log_debug():
            return

        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        self._logger.debug(
            "Response: %s %s status=%s body=%s",
            method,
            url,
            response.status_code,
            self._format_for_logging(payload),
        )

    def _sync_time(self):
        try:
            response = self._session.get(self._base_url + "time")
            server_time = response.json()["serverTime"]
            self._time_offset = server_time - int(time.time() * 1000)
            if self._should_log_debug():
                self._logger.debug("Synchronized server time offset=%sms", self._time_offset)
        except Exception as exc:
            if self._should_log_debug():
                self._logger.debug("Failed to synchronize server time: %s", exc)

    def _sign_request(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000) + self._time_offset
        params.setdefault("recvWindow", self._recv_window)
        query_string = urlencode(params)
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _handle_response(self, response: requests.Response):
        if not (200 <= response.status_code < 300):
            raise DzengiAPIException(response)
        try:
            return response.json()
        except Exception as e:
            raise DzengiRequestException(f"Invalid JSON response: {e}")

    def _request(self, method: str, endpoint: str, signed: bool, **kwargs):
        url = self._base_url + endpoint

        for attempt in range(2):
            params = {k: v for k, v in (kwargs.get("params") or {}).items() if v is not None}
            data = {k: v for k, v in (kwargs.get("data") or {}).items() if v is not None}

            if signed:
                if method in ("POST", "PUT") and data:
                    data = self._sign_request(data)
                else:
                    params = self._sign_request(params)

            self._log_request(method, url, params, data, attempt)

            try:
                if method == "GET":
                    response = self._session.get(url, params=params)
                elif method == "POST":
                    response = self._session.post(url, data=data, params=params)
                elif method == "PUT":
                    response = self._session.put(url, data=data, params=params)
                elif method == "DELETE":
                    response = self._session.delete(url, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            except requests.exceptions.RequestException as e:
                if self._should_log_debug():
                    self._logger.debug("Request failed: %s %s error=%s", method, url, e)
                raise DzengiRequestException(str(e))

            self._log_response(method, url, response)

            if signed and attempt == 0 and response.status_code == 400:
                try:
                    if response.json().get("code") == -1021:
                        if self._should_log_debug():
                            self._logger.debug("Detected timestamp mismatch; synchronizing server time before retry")
                        self._sync_time()
                        continue
                except Exception:
                    pass

            return self._handle_response(response)

    def _get(self, endpoint, params=None, signed=False):
        return self._request("GET", endpoint, signed, params=params or {})

    def _post(self, endpoint, data=None, signed=False):
        return self._request("POST", endpoint, signed, data=data or {})

    def _put(self, endpoint, data=None, signed=False):
        return self._request("PUT", endpoint, signed, data=data or {})

    def _delete(self, endpoint, params=None, signed=False):
        return self._request("DELETE", endpoint, signed, params=params or {})

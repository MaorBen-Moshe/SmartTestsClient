from __future__ import annotations

import os
import urllib
import uuid
from typing import Any

from flask import request

from app.constants.constants import SESSION_ID_KEY, FLASK_REQUEST_ID_KEY


class Utils:
    """A class that provides various utility methods."""

    @staticmethod
    def create_filter_by_list(values: list[str] | None) -> str:
        """Creates a regular expression filter from a list of values.

        Args:
            values (list[str] | None): A list of strings to filter by, or None.

        Returns:
            str: A regular expression that matches any of the values, or an empty string if values is None or empty.
        """
        values = values if values is not None else []
        return "|".join(f".*{value}.*" for value in values)

    @staticmethod
    def is_valid_url(url):
        """Checks if a URL is valid and has a supported extension.

        Args:
            url: The URL to check.

        Returns:
            bool: True if the URL is valid and has a .zip or .html extension, False otherwise.
        """
        parsed = urllib.parse.urlparse(url)
        ext = os.path.splitext(parsed.path)[1]
        return ext in [".zip", ".html"]

    @staticmethod
    def add_flows_without_duplications(flows: list[str], curr_flows: list[str] | None) -> None:
        """Adds flows to a list without duplicating existing ones.

        Args:
            flows (list[str]): The list of flows to add to.
            curr_flows (list[str] | None): The list of flows to add from, or None.

        Returns:
            None: The method modifies the flows list in place.
        """
        curr_flows = curr_flows if curr_flows is not None else []
        flows.extend(curr_flow for curr_flow in curr_flows if curr_flow not in flows)

    @staticmethod
    def get_request_id():
        """Gets the request ID from the flask global object, or generates a new one if not found.

        Returns:
            str: The request ID, a 10-digit hexadecimal string.
        """
        if getattr(request, FLASK_REQUEST_ID_KEY, None):
            return request.request_id

        new_uuid = uuid.uuid4().hex[:10]
        request.request_id = new_uuid

        return new_uuid

    @staticmethod
    def get_session_id_or_default(data: dict[str, Any]):
        """Gets the session ID from a data dictionary, or generates a default one if not found.

        Args:
            data (dict[str, Any]): The data dictionary to look for the session ID.

        Returns:
            str: The session ID, or a randomly generated UUID string if not found.
        """
        return str(data.get(SESSION_ID_KEY)) if data.get(SESSION_ID_KEY) else uuid.uuid4().__str__()

    @staticmethod
    def merge_list(list_to: list[str], list_from: list[str]) -> list[str]:
        """Merges two lists of strings into one, removing duplicates.

        Args:
            list_to (list[str]): The list to merge to, or None.
            list_from (list[str]): The list to merge from, or None.

        Returns:
            list[str]: The merged list of unique strings, or an empty list if both lists are None or empty.
        """
        list_to = list_to if list_to is not None else []
        list_from = list_from if list_from is not None else []
        return list(set(list_to + list_from))

    @staticmethod
    def make_cache_key_smart_get_all(*args, **kwargs):
        """Makes a cache key for the smart_get_all method.

        Args:
            *args: The positional arguments passed to the smart_get_all method.
            **kwargs: The keyword arguments passed to the smart_get_all method.

        Returns:
            str: The cache key, which is based on the second positional argument if it exists and is not None or empty,
            or "empty_args" otherwise.
        """
        suffix = args[1] if len(args) > 1 and args[1] is not None and len(args[1]) > 0 else "empty_args"
        return f"smart_tests_all_{suffix}"

    @staticmethod
    def make_cache_key_smart_analyze_flows(*args, **kwargs):
        """Makes a cache key for the smart_analyze_flows method.

        Args:
            *args: The positional arguments passed to the smart_analyze_flows method.
            **kwargs: The keyword arguments passed to the smart_analyze_flows method.

        Returns:
            str: The cache key, which is based on the concatenation of all positional arguments except the first one, or "empty_args" if none of them exist or are not None or empty.
        """
        args_as_string = (val if val is not None and len(val) > 0 else "none" for val in args[1:])
        suffix = '_'.join(args_as_string)
        suffix = suffix if suffix is not None and len(suffix) > 0 else "empty_args"
        return f"smart_analyze_flows_{suffix}"

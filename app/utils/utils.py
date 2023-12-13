from __future__ import annotations

import os
import urllib
import uuid
from typing import Any

import flask

from app.constants.constants import SESSION_ID_KEY, FLASK_REQUEST_ID_KEY
from app.models.supported_groups import SupportedGroups


class Utils:
    @staticmethod
    def create_filter_by_list(values: list[str] | None) -> str:
        values = values if values is not None else []
        return "|".join([f".*{value}.*" for value in values])

    @staticmethod
    def is_valid_url(url):
        parsed = urllib.parse.urlparse(url)
        ext = os.path.splitext(parsed.path)[1]
        return ext in [".zip", ".html"]

    @staticmethod
    def serialize_class(cls, ignored_fields: list[str]):
        if cls is None:
            return None

        return (dict(
            (i.replace(cls.__class__.__name__, '').lstrip("_"), value)
            for i, value in cls.__dict__.items()
            if i.replace(cls.__class__.__name__, '').lstrip("_") not in ignored_fields
        ))

    @staticmethod
    def add_flows_without_duplications(flows: list[str], curr_flows: list[str] | None) -> None:
        curr_flows = curr_flows if curr_flows is not None else []
        flows.extend([curr_flow for curr_flow in curr_flows if curr_flow not in flows])

    @staticmethod
    def get_request_id():
        if getattr(flask.g, FLASK_REQUEST_ID_KEY, None):
            return flask.g.request_id

        new_uuid = uuid.uuid4().hex[:10]
        flask.g.request_id = new_uuid

        return new_uuid

    @staticmethod
    def get_session_id_or_default(data: dict[str, Any]):
        return data.get(SESSION_ID_KEY) if data.get(SESSION_ID_KEY) else uuid.uuid4()

    @staticmethod
    def merge_list(list_to: list[str], list_from: list[str]) -> list[str]:
        list_to = list_to if list_to is not None else []
        list_from = list_from if list_from is not None else []
        return list(set(list_to + list_from))

    @staticmethod
    def get_project_name_from_supported_group(service_name: str | None, supported_groups: SupportedGroups):
        project = None
        if service_name:
            for group_name in supported_groups:
                group = supported_groups.get_item(group_name)
                if service_name in group.filtered_ms_list:
                    project = group.project
                    break

        return project

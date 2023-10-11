import pytest

from constants.constants import SUPPORTED_GROUPS
from exceptions.excpetions import BadRequest
from tests.test_base import TestBase
from steps.check_analyze_input import CheckAnalyzeClientInput


class TestCheckAnalyzeInput(TestBase):
    def test_check_input_success(self):

        req_data = {
            "buildURL": "build_url",
            "groupName": SUPPORTED_GROUPS[0],
        }

        try:
            CheckAnalyzeClientInput.check_input(req_data)
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            assert True

    def test_check_input_input_is_none(self):
        try:
            CheckAnalyzeClientInput.check_input(None)
        except BadRequest as bre:
            assert f"{bre}" == "No payload provided."
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

    def test_check_input_input_is_empty_dict(self):
        try:
            CheckAnalyzeClientInput.check_input({})
        except BadRequest as bre:
            assert f"{bre}" == "No payload provided."
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

    def test_check_input_input_is_build_url_none(self):
        try:
            data = {
                "groupName": SUPPORTED_GROUPS[0],
            }

            CheckAnalyzeClientInput.check_input(data)
        except BadRequest as bre:
            assert f"{bre}" == "No build url provided."
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

    def test_check_input_input_is_build_url_empty(self):
        try:
            data = {
                "buildURL": "",
                "groupName": SUPPORTED_GROUPS[0],
            }

            CheckAnalyzeClientInput.check_input(data)
        except BadRequest as bre:
            assert f"{bre}" == "No build url provided."
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

    def test_check_input_input_is_group_name_none(self):
        try:
            data = {
                "buildURL": "build_url",
            }

            CheckAnalyzeClientInput.check_input(data)
        except BadRequest as bre:
            assert f"{bre}" == f"Group Name: 'None' is not supported. supported groups: {SUPPORTED_GROUPS}"
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

    def test_check_input_input_is_group_name_not_supported(self):
        try:
            data = {
                "buildURL": "build_url",
                "groupName": SUPPORTED_GROUPS[0] + "_NotSupported"
            }

            CheckAnalyzeClientInput.check_input(data)
        except BadRequest as bre:
            assert f"{bre}" == (f"Group Name: '{SUPPORTED_GROUPS[0] + '_NotSupported'}' is not supported. supported "
                                f"groups: {SUPPORTED_GROUPS}")
        except Exception as ex:
            pytest.fail(f"Error: {ex}")
        else:
            pytest.fail("No error thrown from check_analyze_input")

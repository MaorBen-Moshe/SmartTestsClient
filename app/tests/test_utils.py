import pytest

from app.models.service_data import ServiceData
from test_base import TestBase
from app.utils.utils import Utils


class TestUtils(TestBase):

    def test_create_filter_by_list(self):
        @pytest.mark.parametrize("values, expected", [
            (None, ""),
            ([], ""),
            (["a"], ".*a.*"),
            (["a", "b"], ".*a.*|.*b.*"),
            (["a", "b", "c"], ".*a.*|.*b.*|.*c.*")
        ])
        def test(values, expected):
            result = Utils.create_filter_by_list(values)

            self.assertEqual(result, expected)

    def test_is_valid_url(self):
        @pytest.mark.parametrize("url, expected", [
            ("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4-include-ed/lastSuccessfulBuild/BuildReport"
             "/*zip*/BuildReport.zip", True),
            ("https://www.python.org/", False),
            ("https://realpython.com/pytest-python-testing/", False),
            ("https://docs.pytest.org/en/7.1.x/how-to/unittest.html", False),
            ("https://github.com/pytest-dev/pytest/archive/refs/tags/7.1.1.zip", True),
            ("https://raw.githubusercontent.com/pytest-dev/pytest/main/tox.ini", False),
            ("https://raw.githubusercontent.com/pytest-dev/pytest/main/setup.cfg", False),
            ("https://raw.githubusercontent.com/pytest-dev/pytest/main/pyproject.toml", False)
        ])
        def test(url, expected):
            result = Utils.is_valid_url(url)

            self.assertEqual(result, expected)

    def test_serialize_class(self):
        class WithoutProperties:
            def __init__(self, name, age, gender):
                self._name = name
                self._age = age
                self.gender = gender

        @pytest.mark.parametrize("cls, ignore_fields, expected", [
            (ServiceData.create().old_version("old_version").new_version("new_version").build(),
             [],
             {"old_version": "old_version", "new_version": "new_version"}),
            (ServiceData.create().old_version("old_version").new_version("new_version").build(),
             ['_old_version'],
             {"new_version": "new_version"}),
            (WithoutProperties("Alice", 25, "female"),
             [],
             {"name": "Alice", "age": 25, "gender": "female"}),
            (None, [], None)
        ])
        def test(cls, ignore_fields, expected):
            res = Utils.serialize_class(cls, ignore_fields)

            self.assertEqual(res, expected)

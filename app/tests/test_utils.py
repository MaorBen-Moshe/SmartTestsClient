from parameterized import parameterized

from app.models.service_data import ServiceData
from app.utils.utils import Utils
from test_base import TestBase


class TestUtils(TestBase):
    class WithoutProperties:
        def __init__(self, name, age, gender):
            self._name = name
            self._age = age
            self.gender = gender

    @parameterized.expand([
        (None, ""),
        ([], ""),
        (["a"], ".*a.*"),
        (["a", "b"], ".*a.*|.*b.*"),
        (["a", "b", "c"], ".*a.*|.*b.*|.*c.*")
    ])
    def test_create_filter_by_list(self, values, expected):
        result = Utils.create_filter_by_list(values)

        self.assertEqual(result, expected)

    @parameterized.expand([
        ("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild/BuildReport"
         "/*zip*/BuildReport.zip", True),
        ("https://www.python.org/", False),
        ("https://realpython.com/pytest-python-testing/", False),
        ("https://docs.pytest.org/en/7.1.x/how-to/unittest.html", True),
        ("https://github.com/pytest-dev/pytest/archive/refs/tags/7.1.1.zip", True),
        ("https://raw.githubusercontent.com/pytest-dev/pytest/main/tox.ini", False),
        ("https://raw.githubusercontent.com/pytest-dev/pytest/main/setup.cfg", False),
        ("https://raw.githubusercontent.com/pytest-dev/pytest/main/pyproject.toml", False)
    ])
    def test_is_valid_url(self, url, expected):
        result = Utils.is_valid_url(url)

        self.assertEqual(result, expected)

    @parameterized.expand([
        (ServiceData.create().old_version("old_version").new_version("new_version").build(),
         [],
         {"old_version": "old_version", "new_version": "new_version"}),
        (ServiceData.create().old_version("old_version").new_version("new_version").build(),
         ['old_version'],
         {"new_version": "new_version"}),
        (WithoutProperties("Alice", 25, "female"),
         [],
         {"name": "Alice", "age": 25, "gender": "female"}),
        (None, [], None)
    ])
    def test_serialize_class(self, cls, ignore_fields, expected):
        res = Utils.serialize_class(cls, ignore_fields)

        self.assertEqual(res, expected)

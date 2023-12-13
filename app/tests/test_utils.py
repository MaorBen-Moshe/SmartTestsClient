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
        (ServiceData.create().to_version("to_version").from_version("from_version").project('project').build(),
         [],
         {"to_version": "to_version", "from_version": "from_version", "flows": [], "project": "project"}),
        (ServiceData.create().to_version("to_version").from_version("from_version").build(),
         ['to_version'],
         {"from_version": "from_version", "flows": [], "project": None}),
        (WithoutProperties("Alice", 25, "female"),
         [],
         {"name": "Alice", "age": 25, "gender": "female"}),
        (None, [], None)
    ])
    def test_serialize_class(self, cls, ignore_fields, expected):
        res = Utils.serialize_class(cls, ignore_fields)

        self.assertEqual(res, expected)

    @parameterized.expand([
        (["flow1", "flow2"], None, ["flow1", "flow2"]),
        (["flow1", "flow2"], [], ["flow1", "flow2"]),
        (["flow1", "flow2"], ["flow3", "flow4"], ["flow1", "flow2", "flow3", "flow4"]),
        (["flow1", "flow2"], ["flow1", "flow2"], ["flow1", "flow2"]),
        (["flow1", "flow2"], ["flow1", "flow3"], ["flow1", "flow2", "flow3"]),
        ([], ["flow1", "flow2"], ["flow1", "flow2"])
    ])
    def test_add_flows_without_duplications(self, flows, curr_flows, expected):
        Utils.add_flows_without_duplications(flows, curr_flows)

        self.assertEqual(flows, expected)

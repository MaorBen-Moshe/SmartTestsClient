from parameterized import parameterized

from app.models.group_data import GroupData
from app.models.serializable_model import Serializable
from app.models.service_data import ServiceData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.utils.utils import Utils
from test_base import TestBase


class TestUtils(TestBase):
    class WithoutProperties(Serializable):
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
        (ServiceData.create()
         .to_version("to_version")
         .from_version("from_version")
         .project("project")
         .pull_request_id("pull_request_id")
         .build(),
         {"service_name": None,
          "to": "to_version",
          "from": "from_version",
          "flows": [],
          "project": "project",
          "pullRequestId": "pull_request_id"}),
        (ServiceData.create().to_version("to_version").from_version("from_version").build(),
         {"service_name": None, "to": "to_version", "from": "from_version", "flows": [], "project": None,
          "pullRequestId": None}),
        (WithoutProperties("Alice", 25, "female"),
         {"name": "Alice", "age": 25, "gender": "female"}),
        (None, None),
        (SmartAnalyzeResponse.create()
         .services([ServiceData.create().to_version("to_version").from_version("from_version").build()])
         .total_flows_count(1)
         .curr_flows_count(1)
         .groups({"group1": GroupData.create().flows(["flow1"]).total_flows_count(1).build()})
         .build(),
         {"total_flows_count": 1, "curr_flows_count": 1,
          "groups": {"group1": {"flows": ["flow1"], "curr_flows_count": 1,
                                "total_flows_count": 1,
                                "test_xml_name": None, "test_xml_path": None}},
          "services": [{"service_name": None, "to": "to_version", "from": "from_version", "flows": [],
                        "project": None, "pullRequestId": None}]})
    ])
    def test_serialize_class(self, cls, expected):
        res = cls.toJSON() if cls else None

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

    @parameterized.expand([
        (["flow1", "flow2"], None, ["flow1", "flow2"]),
        (["flow1", "flow2"], [], ["flow1", "flow2"]),
        (["flow1", "flow2"], ["flow3", "flow4"], ["flow1", "flow2", "flow3", "flow4"]),
        (["flow1", "flow2"], ["flow1", "flow2"], ["flow1", "flow2"]),
        (["flow1", "flow2"], ["flow1", "flow3"], ["flow1", "flow2", "flow3"]),
        ([], ["flow1", "flow2"], ["flow1", "flow2"])
    ])
    def test_merge_list(self, list_to, list_from, expected):
        result = Utils.merge_list(list_to, list_from)

        result = sorted(result)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ("productconfigurator", "DIGOC"),
        ("", None),
        (None, None)
    ])
    def test_get_project_name_from_supported_group(self, service_name, expected):
        result = Utils.get_project_name_from_supported_group(service_name, self.config.get_supported_groups())

        self.assertEqual(result, expected)

    @parameterized.expand([
        None,
        ([],)
    ])
    def test_get_project_name_from_supported_group_empty(self, supported_groups):
        result = Utils.get_project_name_from_supported_group('service1', supported_groups)

        self.assertIsNone(result)

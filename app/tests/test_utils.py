from parameterized import parameterized

from app.models.group_data import GroupData
from app.models.serializable_model import Serializable
from app.models.service_data import ServiceData
from app.models.smart_analyze_response import SmartAnalyzeResponse
from app.utils.utils import Utils
from test_base import TestBase


class TestUtils(TestBase):
    class WithoutProperties(Serializable):

        # slots
        __slots__ = [
            "_name",
            "_age",
            "gender"
        ]

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
         {"to": "to_version",
          "from": "from_version",
          "project": "project",
          "pullRequestId": "pull_request_id"}),
        (ServiceData.create().to_version("to_version").from_version("from_version").build(),
         {"to": "to_version", "from": "from_version"}),
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
                                "total_flows_count": 1}},
          "services": [{"to": "to_version", "from": "from_version"}]})
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
        (["smart", "foo"], "smart_tests_all_foo"),
        (["smart", None], "smart_tests_all_empty_args"),
        (["smart"], "smart_tests_all_empty_args"),
        (["smart", ""], "smart_tests_all_empty_args"),
    ])
    def test_make_cache_key_smart_get_all(self, args, expected):
        output = Utils.make_cache_key_smart_get_all(*args)

        self.assertEqual(output, expected)

    @parameterized.expand([
        (["smart", "foo", "bar"], "smart_analyze_flows_foo_bar"),
        (["smart", None, "bar"], "smart_analyze_flows_none_bar"),
        (["smart", "", "bar"], "smart_analyze_flows_none_bar"),
        (["smart"], "smart_analyze_flows_empty_args"),
    ])
    def test_make_cache_key_smart_analyze_flows(self, args, expected):
        output = Utils.make_cache_key_smart_analyze_flows(*args)

        self.assertEqual(output, expected)

    @parameterized.expand([
        ("noCache", True),
        ("noCache1", False),
        ("param1, NoCache", False),
        ("", False),
        (None, False),
    ])
    def test_is_mask_contains_no_cache(self, mask, expected):
        output = Utils.is_mask_contains_no_cache(mask)

        self.assertEqual(output, expected)

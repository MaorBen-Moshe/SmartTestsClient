import pytest

from tests.test_base import TestBase


class TestEndpoints(TestBase):

    def test_supported_groups_endpoint_success(self):
        res = self.client_fixture.get("/supported-groups")
        assert res.status_code == 200
        assert b'["oc-cd-group4-coc-include-ed"]\n' == res.data

    # TODO fix test
    @pytest.mark.skip(reason="need to implement mocks and asserts")
    def test_smart_tests_analyze_endpoint_success(self):
        data = {
            "buildURL": "http://testurl.com",
            "groupName": "oc-cd-group4-coc-include-ed",
        }

        res = self.client_fixture.post("/smart-tests-analyze", json=data, content_type='application/json')
        assert res.status_code == 200

    def test_smart_tests_analyze_endpoint_missing_payload(self):
        res = self.client_fixture.post("/smart-tests-analyze", content_type='application/json')
        assert res.status_code == 400
        assert (b'Error: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.'
                == res.data)

    def test_smart_tests_analyze_endpoint_missing_buildUrl(self):
        data = {
            "groupName": "group_name",
        }

        res = self.client_fixture.post("/smart-tests-analyze", json=data, content_type='application/json')
        assert res.status_code == 400
        assert b'Error: No build url provided.' == res.data

    def test_smart_tests_analyze_endpoint_missing_groupName(self):
        data = {
            "buildURL": "build_url",
        }

        res = self.client_fixture.post("/smart-tests-analyze", json=data, content_type='application/json')
        assert res.status_code == 400
        assert (b"Error: Group Name: 'None' is not supported. supported groups: ['oc-cd-group4-coc-include-ed']"
                == res.data)

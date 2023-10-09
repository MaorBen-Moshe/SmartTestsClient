import pytest


def test_supported_groups_endpoint_success(client):
    res = client.get("/supported-groups")
    assert res.status_code == 200
    assert b'["oc-cd-group4-coc-include-ed"]\n' == res.data


# TODO fix test
@pytest.mark.skip(reason="need to implement mocks and asserts")
def test_smart_tests_analyze_endpoint_success(client):
    data = {
        "buildURL": "",
        "groupName": "oc-cd-group4-coc-include-ed",
    }

    res = client.post("/smart-tests-analyze", json=data, content_type='application/json')
    assert res.status_code == 200


def test_smart_tests_analyze_endpoint_missing_payload(client):
    res = client.post("/smart-tests-analyze", content_type='application/json')
    assert res.status_code == 400
    assert (b'Error: 400 Bad Request: The browser (or proxy) sent a request that this server could not understand.'
            == res.data)


def test_smart_tests_analyze_endpoint_missing_buildUrl(client):
    data = {
        "groupName": "group_name",
    }

    res = client.post("/smart-tests-analyze", json=data, content_type='application/json')
    assert res.status_code == 400
    assert b'Error: No build url provided.' == res.data


def test_smart_tests_analyze_endpoint_missing_groupName(client):
    data = {
        "buildURL": "build_url",
    }

    res = client.post("/smart-tests-analyze", json=data, content_type='application/json')
    assert res.status_code == 400
    assert b"Error: Group Name: 'None' is not supported. supported groups: ['oc-cd-group4-coc-include-ed']" == res.data

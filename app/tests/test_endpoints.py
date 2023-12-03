from test_base import TestUnitBase


class TestEndpointsUnit(TestUnitBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_supported_groups_endpoint_success(self):
        res = self.client_fixture.get("/supported-groups", query_string={"api_key": self.config.get_user_api_token()})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(b'{"oc-cd-group4":{"cluster":"ilocpde456",'
                         b'"group_name":"oc-cd-group4",'
                         b'"url":"http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/"}}\n',
                         res.data)

    def test_supported_groups_endpoint_missing_api_key(self):
        res = self.client_fixture.get("/supported-groups")

        self.assertEqual(res.status_code, 401)

    def test_smart_tests_analyze_endpoint_success(self):
        # parameters
        data = {
            "buildURL": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild"
                        "/BuildReport/*zip*/BuildReport.zip",
            "groupName": "oc-cd-group4",
            "sessionID": "session_id",
        }

        # execute
        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=data,
                                       content_type='application/json',
                                       query_string={"api_key": self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(57, res.json['total_flows_count'])
        self.assertEqual(2, res.json['curr_flows_count'])
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 2)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
        self.assertListEqual(body['extended_mat_7b_APIGW_testng.xml']['flows'], [])
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_name'], 'extended_mat_7b_APIGW_testng.xml')
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')
        self.assertIn('mat_APIGW_testng.xml', body)
        self.assertEqual(body['mat_APIGW_testng.xml']['curr_flows_count'], 2)
        self.assertEqual(body['mat_APIGW_testng.xml']['total_flows_count'], 12)
        self.assertListEqual(body['mat_APIGW_testng.xml']['flows'],
                             ['com.amdocs.core.oc.test.flows.schedulerTask.RetrieveSchedulerTaskFlow',
                              'com.amdocs.core.oc.test.flows.discovery.categories.BrowsingCategoriesSelfServiceFlows'])
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_name'], 'mat_APIGW_testng.xml')
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')

        self.assertEqual(10, self.mock_nexus_search.call_count)
        self.mock_get_html.assert_called_once_with("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4"
                                                   "/lastSuccessfulBuild/BuildReport/*zip*/BuildReport.zip")
        self.mock_get_all_flows.assert_called_once_with(".*group4_integration_tests_testng.*|.*mat_APIGW_testng"
                                                        ".*|.*extended_mat_7a_APIGW_testng.*|"
                                                        ".*extended_mat_7b_APIGW_testng.*|.*extended_mat_APIGW_testng"
                                                        ".*|.*shared_regression_testng"
                                                        ".*|.*grp4_integration_to_CT_testng"
                                                        ".*|.*ContratedOffer_tests_testng"
                                                        ".*|.*ContratedOffer_Pack_testng"
                                                        ".*|.*Everest_Configurator_Pack_testng"
                                                        ".*|.*Everest_Qualification_Pack_testng"
                                                        ".*|.*Everest_validator_pack"
                                                        ".*|.*Olympus_pack_testng"
                                                        ".*|.*Everest_Validator_Dependency_Rules_Pack_testng"
                                                        ".*|.*Fuji_Price_Pack_testng"
                                                        ".*|.*Fuji_Promotion_Pack_testng"
                                                        ".*|.*Fuji_Replace_Pack_testng"
                                                        ".*|.*mat_oc_product_configurator_hooks_APIGW_testng.*")

        self.mock_analyze_flows.assert_called_once()
        args, kwargs = self.mock_analyze_flows.call_args
        self.assertEqual(len(args), 4)
        self.assertEqual(args[0], "productconfigurator")
        self.assertEqual(args[1], "0.67.18")
        self.assertEqual(args[2], "0.67.19")
        self.assertEqual(args[3], ".*group4_integration_tests_testng.*|.*mat_APIGW_testng"
                                  ".*|.*extended_mat_7a_APIGW_testng.*|"
                                  ".*extended_mat_7b_APIGW_testng.*|.*extended_mat_APIGW_testng"
                                  ".*|.*shared_regression_testng"
                                  ".*|.*grp4_integration_to_CT_testng"
                                  ".*|.*ContratedOffer_tests_testng"
                                  ".*|.*ContratedOffer_Pack_testng"
                                  ".*|.*Everest_Configurator_Pack_testng"
                                  ".*|.*Everest_Qualification_Pack_testng"
                                  ".*|.*Everest_validator_pack"
                                  ".*|.*Olympus_pack_testng"
                                  ".*|.*Everest_Validator_Dependency_Rules_Pack_testng"
                                  ".*|.*Fuji_Price_Pack_testng"
                                  ".*|.*Fuji_Promotion_Pack_testng"
                                  ".*|.*Fuji_Replace_Pack_testng"
                                  ".*|.*mat_oc_product_configurator_hooks_APIGW_testng.*")

    def test_smart_tests_analyze_endpoint_success_same_versions(self):
        # parameters
        data = {
            "buildURL": "http://test_html_same_version/zipfile.zip",
            "groupName": "oc-cd-group4",
            "sessionID": "session_id",
        }

        # execute
        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=data,
                                       content_type='application/json',
                                       query_string={"api_key": self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(57, res.json['total_flows_count'])
        self.assertEqual(0, res.json['curr_flows_count'])
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 2)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
        self.assertListEqual(body['extended_mat_7b_APIGW_testng.xml']['flows'], [])
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_name'], 'extended_mat_7b_APIGW_testng.xml')
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')
        self.assertIn('mat_APIGW_testng.xml', body)
        self.assertEqual(body['mat_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['mat_APIGW_testng.xml']['total_flows_count'], 12)
        self.assertListEqual(body['mat_APIGW_testng.xml']['flows'], [])
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_name'], 'mat_APIGW_testng.xml')
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')

        self.assertEqual(10, self.mock_nexus_search.call_count)
        self.mock_get_html.assert_called_once_with("http://test_html_same_version/zipfile.zip")
        self.mock_get_all_flows.assert_called_once_with(".*group4_integration_tests_testng.*|.*mat_APIGW_testng"
                                                        ".*|.*extended_mat_7a_APIGW_testng.*|"
                                                        ".*extended_mat_7b_APIGW_testng.*|.*extended_mat_APIGW_testng"
                                                        ".*|.*shared_regression_testng"
                                                        ".*|.*grp4_integration_to_CT_testng"
                                                        ".*|.*ContratedOffer_tests_testng"
                                                        ".*|.*ContratedOffer_Pack_testng"
                                                        ".*|.*Everest_Configurator_Pack_testng"
                                                        ".*|.*Everest_Qualification_Pack_testng"
                                                        ".*|.*Everest_validator_pack"
                                                        ".*|.*Olympus_pack_testng"
                                                        ".*|.*Everest_Validator_Dependency_Rules_Pack_testng"
                                                        ".*|.*Fuji_Price_Pack_testng"
                                                        ".*|.*Fuji_Promotion_Pack_testng"
                                                        ".*|.*Fuji_Replace_Pack_testng"
                                                        ".*|.*mat_oc_product_configurator_hooks_APIGW_testng.*")

        self.mock_analyze_flows.assert_not_called()

    def test_smart_tests_analyze_endpoint_missing_payload(self):
        res = self.client_fixture.post("/smart-tests-analyze",
                                       content_type='application/json',
                                       query_string={"api_key": self.config.get_user_api_token()})
        self.assertEqual(res.status_code, 400)
        self.assertEqual((b'[ERROR] 400 Bad Request: The browser (or proxy) sent a request that this server could not '
                          b'understand.'), res.data)

    def test_smart_tests_analyze_endpoint_missing_buildUrl(self):
        data = {
            "groupName": "group_name",
        }

        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=data,
                                       content_type='application/json',
                                       query_string={"api_key": self.config.get_user_api_token()})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(b'[ERROR] 400: No build url provided.', res.data)

    def test_smart_tests_analyze_endpoint_missing_groupName(self):
        data = {
            "buildURL": "build_url",
        }

        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=data,
                                       content_type='application/json',
                                       query_string={"api_key": self.config.get_user_api_token()})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(b"[ERROR] 400: Group Name: 'None' is not supported.", res.data)

    def test_smart_tests_analyze_endpoint_missing_api_key(self):
        # parameters
        data = {
            "buildURL": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild"
                        "/BuildReport/*zip*/BuildReport.zip",
            "groupName": "oc-cd-group4",
        }

        # execute
        res = self.client_fixture.post("/smart-tests-analyze", json=data, content_type='application/json')

        # asserts
        self.assertEqual(res.status_code, 401)

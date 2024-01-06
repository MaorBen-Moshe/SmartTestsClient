from parameterized import parameterized

from app.constants.constants import API_KEY_QUERY_PARAM
from app.models.service_data import ServiceData
from test_base import TestUnitBase


class TestEndpointsUnit(TestUnitBase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_supported_groups_endpoint_success(self):
        with self.assertLogs(self.logger.get_logger_name(), level='DEBUG') as cm:
            res = self.client_fixture.get("/supported-groups",
                                          headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(res.json)
            self.assertEqual(len(res.json), 1)
            self.assertIn('oc-cd-group4', res.json)
            self.assertEqual(res.json['oc-cd-group4']['group_name'], 'oc-cd-group4')
            self.assertEqual(res.json['oc-cd-group4']['cluster'], 'ilocpde456')
            self.assertEqual(res.json['oc-cd-group4']['url'],
                             'http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/')
            self.assertEqual(res.json['oc-cd-group4']['project'], 'DIGOC')
            self.assertEqual(len(res.json['oc-cd-group4']['ms_list']), 12)
            self.assertEqual(len(res.json['oc-cd-group4']['test_files']), 22)

            self.assertEqual(cm.output,
                             ['DEBUG:app:Supported groups request.', "DEBUG:app:Supported groups response. response={"
                                                                     "'oc-cd-group4': {'group_name': 'oc-cd-group4', "
                                                                     "'cluster': 'ilocpde456', 'test_files': ["
                                                                     "'shared_regression_testng', 'mat_APIGW_testng', "
                                                                     "'extended_mat_7a_APIGW_testng', "
                                                                     "'extended_mat_7b_APIGW_testng', "
                                                                     "'extended_mat_APIGW_testng', "
                                                                     "'extended_mat_2_APIGW_testng', "
                                                                     "'extended_mat_3_APIGW_testng', "
                                                                     "'extended_mat_4_APIGW_testng', "
                                                                     "'extended_mat_5_APIGW_testng', "
                                                                     "'group4_integration_tests_testng', "
                                                                     "'grp4_integration_to_CT_testng', "
                                                                     "'ContratedOffer_tests_testng', "
                                                                     "'ContratedOffer_Pack_testng', "
                                                                     "'Everest_Configurator_Pack_testng', "
                                                                     "'Everest_Qualification_Pack_testng', "
                                                                     "'Everest_validator_pack', "
                                                                     "'Olympus_pack_testng', "
                                                                     "'Everest_Validator_Dependency_Rules_Pack_testng"
                                                                     "', 'Fuji_Price_Pack_testng', "
                                                                     "'Fuji_Promotion_Pack_testng', "
                                                                     "'Fuji_Replace_Pack_testng', "
                                                                     "'mat_oc_product_configurator_hooks_APIGW_testng"
                                                                     "'], "
                                                                     "'url': "
                                                                     "'http://illin5565:18080/job/oc-cd-group4/job/oc"
                                                                     "-cd-group4/', 'ms_list': [{'service_name': "
                                                                     "'productconfigurator-subdomain', 'repo_name': "
                                                                     "'productconfigurator-subdomain', 'project': "
                                                                     "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                     "{'service_name': "
                                                                     "'productconfigurator-subdomain-api', "
                                                                     "'repo_name': "
                                                                     "'productconfigurator-subdomain-api', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator', 'repo_name': "
                                                                     "'productconfigurator-ms', 'project': 'DIGOC', "
                                                                     "'related_group': 'oc-cd-group4'}, "
                                                                     "{'service_name': 'productconfigurator-action', "
                                                                     "'repo_name': 'productconfigurator-action-ms', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator-commitmentterm', "
                                                                     "'repo_name': "
                                                                     "'productconfigurator-commitmentterm-ms', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator-mergeentities', "
                                                                     "'repo_name': "
                                                                     "'productconfigurator-mergeentities-ms', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator-pioperations', "
                                                                     "'repo_name': "
                                                                     "'productconfigurator-pioperations-ms', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator-price', 'repo_name': "
                                                                     "'productconfigurator-price-ms', 'project': "
                                                                     "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                     "{'service_name': "
                                                                     "'productconfigurator-promotion', 'repo_name': "
                                                                     "'productconfigurator-promotion-ms', 'project': "
                                                                     "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                     "{'service_name': "
                                                                     "'productconfigurator-qualification', "
                                                                     "'repo_name': "
                                                                     "'productconfigurator-qualification-ms', "
                                                                     "'project': 'DIGOC', 'related_group': "
                                                                     "'oc-cd-group4'}, {'service_name': "
                                                                     "'productconfigurator-replace', 'repo_name': "
                                                                     "'productconfigurator-replace-ms', 'project': "
                                                                     "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                     "{'service_name': 'productvalidator', "
                                                                     "'repo_name': 'productvalidator-ms', 'project': "
                                                                     "'DIGOC', 'related_group': 'oc-cd-group4'}], "
                                                                     "'project': 'DIGOC'}}"])

    def test_supported_groups_endpoint_missing_api_key(self):
        res = self.client_fixture.get("/supported-groups")

        self.assertEqual(res.status_code, 401)

    def test_supported_services_endpoint_success(self):
        with self.assertLogs(self.logger.get_logger_name(), level='DEBUG') as cm:
            res = self.client_fixture.get("/supported-services",
                                          headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(res.json)
            self.assertEqual(len(res.json), 12)
            configurator_service = [service for service in res.json if service['service_name'] == 'productconfigurator']
            self.assertEqual(1, len(configurator_service))
            self.assertEqual(configurator_service[0]['service_name'], 'productconfigurator')
            self.assertEqual(configurator_service[0]['repo_name'], 'productconfigurator-ms')
            self.assertEqual(configurator_service[0]['project'], 'DIGOC')
            self.assertEqual(configurator_service[0]['related_group'], 'oc-cd-group4')
            self.assertEqual(cm.output,
                             ['DEBUG:app:Supported services request.', "DEBUG:app:Supported services response. "
                                                                       "response=[{'service_name': "
                                                                       "'productconfigurator-subdomain', 'repo_name': "
                                                                       "'productconfigurator-subdomain', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-subdomain-api', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-subdomain-api', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator', 'repo_name': "
                                                                       "'productconfigurator-ms', 'project': 'DIGOC', "
                                                                       "'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-action', 'repo_name': "
                                                                       "'productconfigurator-action-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-commitmentterm', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-commitmentterm-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-mergeentities', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-mergeentities-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-pioperations', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-pioperations-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-price', 'repo_name': "
                                                                       "'productconfigurator-price-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-promotion', 'repo_name': "
                                                                       "'productconfigurator-promotion-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-qualification', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-qualification-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-replace', 'repo_name': "
                                                                       "'productconfigurator-replace-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': 'productvalidator', "
                                                                       "'repo_name': 'productvalidator-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}]"])

    def test_supported_services_endpoint_success_filter_group4(self):
        with self.assertLogs(self.logger.get_logger_name(), level='DEBUG') as cm:
            res = self.client_fixture.get("/supported-services?groupName=oc-cd-group4",
                                          headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(res.json)
            self.assertEqual(len(res.json), 12)
            configurator_service = [service for service in res.json if service['service_name'] == 'productconfigurator']
            self.assertEqual(1, len(configurator_service))
            self.assertEqual(configurator_service[0]['service_name'], 'productconfigurator')
            self.assertEqual(configurator_service[0]['repo_name'], 'productconfigurator-ms')
            self.assertEqual(configurator_service[0]['project'], 'DIGOC')
            self.assertEqual(configurator_service[0]['related_group'], 'oc-cd-group4')
            self.assertEqual(cm.output,
                             ['DEBUG:app:Supported services request.', "DEBUG:app:Supported services response. "
                                                                       "response=[{'service_name': "
                                                                       "'productconfigurator-subdomain', 'repo_name': "
                                                                       "'productconfigurator-subdomain', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-subdomain-api', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-subdomain-api', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator', 'repo_name': "
                                                                       "'productconfigurator-ms', 'project': 'DIGOC', "
                                                                       "'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-action', 'repo_name': "
                                                                       "'productconfigurator-action-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-commitmentterm', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-commitmentterm-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-mergeentities', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-mergeentities-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-pioperations', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-pioperations-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-price', 'repo_name': "
                                                                       "'productconfigurator-price-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': "
                                                                       "'productconfigurator-promotion', 'repo_name': "
                                                                       "'productconfigurator-promotion-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-qualification', "
                                                                       "'repo_name': "
                                                                       "'productconfigurator-qualification-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}, {'service_name': "
                                                                       "'productconfigurator-replace', 'repo_name': "
                                                                       "'productconfigurator-replace-ms', 'project': "
                                                                       "'DIGOC', 'related_group': 'oc-cd-group4'}, "
                                                                       "{'service_name': 'productvalidator', "
                                                                       "'repo_name': 'productvalidator-ms', "
                                                                       "'project': 'DIGOC', 'related_group': "
                                                                       "'oc-cd-group4'}]"])

    def test_supported_services_endpoint_not_exist_group(self):
        with self.assertLogs(self.logger.get_logger_name(), level='DEBUG') as cm:
            res = self.client_fixture.get("/supported-services?groupName=notExist",
                                          headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(res.json)
            self.assertEqual(len(res.json), 0)

    def test_supported_services_endpoint_missing_api_key(self):
        res = self.client_fixture.get("/supported-services")

        self.assertEqual(res.status_code, 401)

    def test_smart_tests_analyze_endpoint_success(self):
        with self.assertLogs(self.logger.get_logger_name(), level='INFO') as cm:
            # parameters
            data = {
                "infoLevel": "debug",
                "buildURL": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild"
                            "/BuildReport/*zip*/BuildReport.zip",
                "groupName": "oc-cd-group4",
                "sessionID": "session_id",
            }

            # execute
            res = self.client_fixture.post("/smart-tests-analyze",
                                           json=data,
                                           content_type='application/json',
                                           headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})

            # asserts
            self.assertEqual(res.status_code, 200)
            self.assertIsNotNone(res.json)
            self.assertEqual(57, res.json['total_flows_count'])
            self.assertEqual(2, res.json['curr_flows_count'])
            services = res.json['services']
            self.assertIsNotNone(services)
            self.assertEqual(len(services), 12)
            configurator_service = [service for service in services
                                    if service['service_name'] == 'productconfigurator']
            self.assertEqual(1, len(configurator_service))
            self.assertEqual(configurator_service[0]['from'], '0.67.19')
            self.assertEqual(configurator_service[0]['to'], '0.67.18')
            self.assertEqual(len(configurator_service[0]['flows']), 2)
            body = res.json['groups']
            self.assertIsNotNone(body)
            self.assertEqual(len(body), 2)
            self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
            self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
            self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
            self.assertNotIn('flows', body['extended_mat_7b_APIGW_testng.xml'])
            self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_name'],
                             'extended_mat_7b_APIGW_testng.xml')
            self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')
            self.assertIn('mat_APIGW_testng.xml', body)
            self.assertEqual(body['mat_APIGW_testng.xml']['curr_flows_count'], 2)
            self.assertEqual(body['mat_APIGW_testng.xml']['total_flows_count'], 12)
            self.assertListEqual(body['mat_APIGW_testng.xml']['flows'],
                                 ['com.amdocs.core.oc.test.flows.schedulerTask.RetrieveSchedulerTaskFlow',
                                  'com.amdocs.core.oc.test.flows.discovery.categories'
                                  '.BrowsingCategoriesSelfServiceFlows'])
            self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_name'], 'mat_APIGW_testng.xml')
            self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')

            self.assertEqual(12, self.mock_nexus_search.call_count)
            self.mock_get_html.assert_called_once_with("http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4"
                                                       "/lastSuccessfulBuild/BuildReport/*zip*/BuildReport.zip")
            self.mock_get_all_flows.assert_called_once_with(".*shared_regression_testng.*|.*mat_APIGW_testng.*|"
                                                            ".*extended_mat_7a_APIGW_testng.*|"
                                                            ".*extended_mat_7b_APIGW_testng.*|"
                                                            ".*extended_mat_APIGW_testng.*|"
                                                            ".*extended_mat_2_APIGW_testng.*|"
                                                            ".*extended_mat_3_APIGW_testng.*|"
                                                            ".*extended_mat_4_APIGW_testng.*|"
                                                            ".*extended_mat_5_APIGW_testng.*|"
                                                            ".*group4_integration_tests_testng.*|"
                                                            ".*grp4_integration_to_CT_testng.*|"
                                                            ".*ContratedOffer_tests_testng.*|"
                                                            ".*ContratedOffer_Pack_testng.*|"
                                                            ".*Everest_Configurator_Pack_testng.*|"
                                                            ".*Everest_Qualification_Pack_testng.*|"
                                                            ".*Everest_validator_pack.*|"
                                                            ".*Olympus_pack_testng.*|"
                                                            ".*Everest_Validator_Dependency_Rules_Pack_testng.*|"
                                                            ".*Fuji_Price_Pack_testng.*|"
                                                            ".*Fuji_Promotion_Pack_testng.*|"
                                                            ".*Fuji_Replace_Pack_testng.*|"
                                                            ".*mat_oc_product_configurator_hooks_APIGW_testng.*")

            self.mock_analyze_flows.assert_called_once()
            args, kwargs = self.mock_analyze_flows.call_args
            self.assertEqual(len(args), 6)
            self.assertEqual(args[0], "productconfigurator-ms")
            self.assertEqual(args[1], "DIGOC")
            self.assertEqual(args[2], "0.67.19")
            self.assertEqual(args[3], "0.67.18")
            self.assertEqual(args[4], None)
            self.assertEqual(args[5], ".*shared_regression_testng.*|.*mat_APIGW_testng.*|"
                                      ".*extended_mat_7a_APIGW_testng.*|"
                                      ".*extended_mat_7b_APIGW_testng.*|"
                                      ".*extended_mat_APIGW_testng.*|"
                                      ".*extended_mat_2_APIGW_testng.*|"
                                      ".*extended_mat_3_APIGW_testng.*|"
                                      ".*extended_mat_4_APIGW_testng.*|"
                                      ".*extended_mat_5_APIGW_testng.*|"
                                      ".*group4_integration_tests_testng.*|"
                                      ".*grp4_integration_to_CT_testng.*|"
                                      ".*ContratedOffer_tests_testng.*|"
                                      ".*ContratedOffer_Pack_testng.*|"
                                      ".*Everest_Configurator_Pack_testng.*|"
                                      ".*Everest_Qualification_Pack_testng.*|"
                                      ".*Everest_validator_pack.*|"
                                      ".*Olympus_pack_testng.*|"
                                      ".*Everest_Validator_Dependency_Rules_Pack_testng.*|"
                                      ".*Fuji_Price_Pack_testng.*|"
                                      ".*Fuji_Promotion_Pack_testng.*|"
                                      ".*Fuji_Replace_Pack_testng.*|"
                                      ".*mat_oc_product_configurator_hooks_APIGW_testng.*")

            self.assertListEqual(cm.output, [
                "INFO:app:AnalyzeAppService.analyze(): Processing payload data.",
                "INFO:app:AnalyzeAppService.analyze(): Loading services version from nexus.",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-subdomain",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-subdomain-api",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-action",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-commitmentterm",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-mergeentities",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-price",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-promotion",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-qualification",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productconfigurator-replace",
                "WARNING:app:NexusSearchService._get_service_data_for_each_entry(): Failed to get version for "
                "productvalidator",
                "INFO:app:AnalyzeAppService.analyze(): Loading build report data.",
                "INFO:app:AnalyzeAppService.analyze(): Updating data per group.",
                "INFO:app:AnalyzeAppService.analyze(): Analyzing flows to run.",
                "INFO:app:AnalyzeAppService.analyze(): Preparing response."
            ])

    def test_smart_tests_analyze_endpoint_success_same_versions(self):
        # parameters
        data = {
            "infoLevel": "debug",
            "buildURL": "http://test_html_same_version/zipfile.zip",
            "groupName": "oc-cd-group4",
            "sessionID": "session_id",
        }

        # execute
        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=data,
                                       content_type='application/json',
                                       headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(57, res.json['total_flows_count'])
        self.assertEqual(0, res.json['curr_flows_count'])
        services = res.json['services']
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 12)
        configurator_service = [service for service in services
                                if service['service_name'] == 'productconfigurator']
        self.assertEqual(1, len(configurator_service))
        self.assertEqual(configurator_service[0]['from'], '0.67.19')
        self.assertEqual(configurator_service[0]['to'], '0.67.19')
        self.assertNotIn('flows', configurator_service[0])
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 2)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
        self.assertNotIn('flows', body['extended_mat_7b_APIGW_testng.xml'])
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_name'], 'extended_mat_7b_APIGW_testng.xml')
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')
        self.assertIn('mat_APIGW_testng.xml', body)
        self.assertEqual(body['mat_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['mat_APIGW_testng.xml']['total_flows_count'], 12)
        self.assertNotIn('flows', body['mat_APIGW_testng.xml'])
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_name'], 'mat_APIGW_testng.xml')
        self.assertEqual(body['mat_APIGW_testng.xml']['test_xml_path'], 'com/amdocs/core/oc/testng')

        self.assertEqual(12, self.mock_nexus_search.call_count)
        self.mock_get_html.assert_called_once_with("http://test_html_same_version/zipfile.zip")
        self.mock_get_all_flows.assert_called_once_with(".*shared_regression_testng.*|.*mat_APIGW_testng.*|"
                                                        ".*extended_mat_7a_APIGW_testng.*|"
                                                        ".*extended_mat_7b_APIGW_testng.*|"
                                                        ".*extended_mat_APIGW_testng.*|"
                                                        ".*extended_mat_2_APIGW_testng.*|"
                                                        ".*extended_mat_3_APIGW_testng.*|"
                                                        ".*extended_mat_4_APIGW_testng.*|"
                                                        ".*extended_mat_5_APIGW_testng.*|"
                                                        ".*group4_integration_tests_testng.*|"
                                                        ".*grp4_integration_to_CT_testng.*|"
                                                        ".*ContratedOffer_tests_testng.*|"
                                                        ".*ContratedOffer_Pack_testng.*|"
                                                        ".*Everest_Configurator_Pack_testng.*|"
                                                        ".*Everest_Qualification_Pack_testng.*|"
                                                        ".*Everest_validator_pack.*|"
                                                        ".*Olympus_pack_testng.*|"
                                                        ".*Everest_Validator_Dependency_Rules_Pack_testng.*|"
                                                        ".*Fuji_Price_Pack_testng.*|"
                                                        ".*Fuji_Promotion_Pack_testng.*|"
                                                        ".*Fuji_Replace_Pack_testng.*|"
                                                        ".*mat_oc_product_configurator_hooks_APIGW_testng.*")

        self.mock_analyze_flows.assert_not_called()

    @parameterized.expand([
        ({
             "buildURL": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild"
                         "/BuildReport/*zip*/BuildReport.zip",
             "groupName": "oc-cd-group4",
         }, False, 401, ('[ERROR] 401 Unauthorized: The server could not verify that you are authorize'
                         'd to access the URL requested. You either supplied the wrong credentials (e.'
                         "g. a bad password), or your browser doesn't understand how to supply the cre"
                         'dentials required.')),
        ({
             "buildURL": "build_url",
         }, True, 400, "[ERROR] 400: Group Name: 'None' is not supported."),
        ({
             "groupName": "group_name",
         }, True, 400, "[ERROR] 400: No build url provided."),
        (None, True, 400, '[ERROR] 400 Bad Request: The browser (or proxy) sent a request that this server could not '
                          'understand.')
    ])
    def test_smart_analyze_endpoint_missing_data(self, payload, with_query_param, error_code, error_msg):
        headers = {API_KEY_QUERY_PARAM: self.config.get_user_api_token()} if with_query_param else {}
        res = self.client_fixture.post("/smart-tests-analyze",
                                       json=payload,
                                       content_type='application/json',
                                       headers=headers)
        self.assertEqual(error_code, res.status_code)
        self.assertEqual(error_msg, res.json['error_message'])

    def test_smart_analyze_dev_endpoint_success(self):
        # parameters
        data = {
            "infoLevel": "debug",
            "services": [
                {
                    "name": "productconfigurator",
                    "from": "0.67.20",
                },
                {
                    "name": "productconfigurator-pioperations",
                    "from": "0.67.13",
                    "to": "0.67.11",
                },
            ]
        }

        # execute
        res = self.client_fixture.post("/smart-tests-analyze-dev",
                                       json=data,
                                       content_type='application/json',
                                       headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(712, res.json['total_flows_count'])
        self.assertEqual(2, res.json['curr_flows_count'])
        services = res.json['services']
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 2)
        configurator_service = [service for service in services
                                if service['service_name'] == 'productconfigurator']
        self.assertEqual(1, len(configurator_service))
        self.assertEqual(configurator_service[0]['from'], '0.67.20')
        self.assertEqual(configurator_service[0]['to'], '0.67.19')
        self.assertEqual(len(configurator_service[0]['flows']), 2)
        pioperations_service = [service for service in services
                                if service['service_name'] == 'productconfigurator-pioperations']
        self.assertEqual(1, len(pioperations_service))
        self.assertEqual(pioperations_service[0]['from'], '0.67.13')
        self.assertEqual(pioperations_service[0]['to'], '0.67.11')
        self.assertNotIn('flows', pioperations_service[0])
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 3)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
        self.assertNotIn('flows', ['extended_mat_7b_APIGW_testng.xml'])
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
        self.assertIn('unknown-group', body)
        self.assertEqual(body['unknown-group']['curr_flows_count'], 0)
        self.assertEqual(body['unknown-group']['total_flows_count'], 655)
        self.assertEqual(body['unknown-group']['test_xml_name'], 'unknown-group')
        self.assertEqual(body['unknown-group']['test_xml_path'], '')

        self.mock_nexus_search.assert_called_once_with({'repository': self.config.get_index_data_repository(),
                                                        'name': 'productconfigurator'})
        self.mock_get_all_flows.assert_called_once_with('')
        self.assertEqual(2, self.mock_analyze_flows.call_count)

        calls = [self.mock_analyze_flows.mock_calls[0], self.mock_analyze_flows.mock_calls[1]]

        services_expected = {
            'productconfigurator-ms': ServiceData.create()
            .repo_name('productconfigurator-ms')
            .from_version('0.67.20')
            .to_version('0.67.19')
            .project('DIGOC')
            .build(),
            'productconfigurator-pioperations-ms': ServiceData.create()
            .repo_name('productconfigurator-pioperations-ms')
            .from_version('0.67.13')
            .to_version('0.67.11')
            .project('DIGOC')
            .build()
        }

        for curr_call in calls:
            self.assertEqual(len(curr_call.args), 6)
            expected_service = services_expected.get(curr_call.args[0])
            self.assertIsNotNone(expected_service)
            self.assertEqual(curr_call.args[1], expected_service.project)
            self.assertEqual(curr_call.args[2], expected_service.from_version)
            self.assertEqual(curr_call.args[3], expected_service.to_version)
            self.assertEqual(curr_call.args[4], expected_service.pull_request_id)
            self.assertEqual(curr_call.args[5], '')

    @parameterized.expand([
        ({
             "infoLevel": "debug",
             "services": [
                 {
                     "name": "productconfigurator",
                     "pullRequestId": '12345',
                 }
             ]
         },),
        ({
             "infoLevel": "debug",
             "services": [
                 {
                     "name": "productconfigurator",
                     "from": "0.67.20",
                     "pullRequestId": '12345'
                 }
             ]
         },),
        ({
             "infoLevel": "debug",
             "services": [
                 {
                     "name": "productconfigurator",
                     "from": "0.67.20",
                     "to": "0.67.19",
                     "pullRequestId": '12345'
                 }
             ]
         },)
    ])
    def test_smart_analyze_dev_endpoint_success_pull_request_id(self, data):
        # execute
        res = self.client_fixture.post("/smart-tests-analyze-dev",
                                       json=data,
                                       content_type='application/json',
                                       headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(712, res.json['total_flows_count'])
        self.assertEqual(2, res.json['curr_flows_count'])
        services = res.json['services']
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 1)
        self.assertEqual("productconfigurator", services[0]['service_name'])
        self.assertNotIn('from', services[0])
        self.assertNotIn('to', services[0])
        self.assertEqual(len(services[0]['flows']), 2)
        self.assertEqual(services[0]['pullRequestId'], '12345')
        self.assertEqual(len(services[0]['flows']), 2)
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 3)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
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
        self.assertIn('unknown-group', body)
        self.assertEqual(body['unknown-group']['curr_flows_count'], 0)
        self.assertEqual(body['unknown-group']['total_flows_count'], 655)
        self.assertEqual(body['unknown-group']['test_xml_name'], 'unknown-group')
        self.assertEqual(body['unknown-group']['test_xml_path'], '')

        self.mock_nexus_search.assert_not_called()
        self.mock_get_all_flows.assert_called_once_with('')
        self.assertEqual(1, self.mock_analyze_flows.call_count)
        call_args = self.mock_analyze_flows.mock_calls[0].args
        self.assertEqual(len(call_args), 6)
        self.assertEqual(call_args[0], 'productconfigurator-ms')
        self.assertEqual(call_args[1], 'DIGOC')
        self.assertIsNone(call_args[2])
        self.assertIsNone(call_args[3])
        self.assertEqual(call_args[4], '12345')
        self.assertEqual(call_args[5], '')

    @parameterized.expand([
        ({
             "infoLevel": "debug",
             "services": [
                 {
                     "name": "productconfigurator",
                     "pullRequestId": '12345',
                     "project": "NOT_DIGOC"
                 }
             ]
         },)
    ])
    def test_smart_analyze_dev_endpoint_success_different_project_name(self, data):
        # execute
        res = self.client_fixture.post("/smart-tests-analyze-dev",
                                       json=data,
                                       content_type='application/json',
                                       headers={API_KEY_QUERY_PARAM: self.config.get_user_api_token()})

        # asserts
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json)
        self.assertEqual(712, res.json['total_flows_count'])
        self.assertEqual(2, res.json['curr_flows_count'])
        services = res.json['services']
        self.assertIsNotNone(services)
        self.assertEqual(len(services), 1)
        configurator_service = [service for service in services
                                if service['service_name'] == 'productconfigurator']
        self.assertEqual(1, len(configurator_service))
        self.assertNotIn('from', configurator_service[0])
        self.assertNotIn('to', configurator_service[0])
        self.assertEqual(len(configurator_service[0]['flows']), 2)
        self.assertEqual(configurator_service[0]['pullRequestId'], '12345')
        self.assertEqual(len(configurator_service[0]['flows']), 2)
        body = res.json['groups']
        self.assertIsNotNone(body)
        self.assertEqual(len(body), 3)
        self.assertIn('extended_mat_7b_APIGW_testng.xml', body)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['curr_flows_count'], 0)
        self.assertEqual(body['extended_mat_7b_APIGW_testng.xml']['total_flows_count'], 45)
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
        self.assertIn('unknown-group', body)
        self.assertEqual(body['unknown-group']['curr_flows_count'], 0)
        self.assertEqual(body['unknown-group']['total_flows_count'], 655)
        self.assertNotIn('flows', body['unknown-group'])
        self.assertEqual(body['unknown-group']['test_xml_name'], 'unknown-group')
        self.assertEqual(body['unknown-group']['test_xml_path'], '')

        self.mock_nexus_search.assert_not_called()
        self.mock_get_all_flows.assert_called_once_with('')
        self.assertEqual(1, self.mock_analyze_flows.call_count)
        call_args = self.mock_analyze_flows.mock_calls[0].args
        self.assertEqual(len(call_args), 6)
        self.assertEqual(call_args[0], 'productconfigurator-ms')
        self.assertEquals(call_args[1], 'NOT_DIGOC')
        self.assertIsNone(call_args[2])
        self.assertIsNone(call_args[3])
        self.assertEqual(call_args[4], '12345')
        self.assertEqual(call_args[5], '')

    @parameterized.expand([
        (None, True, 400, '[ERROR] 400 Bad Request: The browser (or proxy) sent a request that this server could not '
                          'understand.'),
        ({
             "services": []
         }, False, 401, ('[ERROR] 401 Unauthorized: The server could not verify that you are authorize'
                         'd to access the URL requested. You either supplied the wrong credentials (e.'
                         "g. a bad password), or your browser doesn't understand how to supply the cre"
                         'dentials required.')),
        ({
             "services": [
                 {
                     "name": "service_name",
                 }
             ]
         }, True, 400, "[ERROR] 400: Service 'service_name' is missing mandatory field: 'from' or 'pullRequestId'."),
    ])
    def test_smart_analyze_dev_endpoint_missing_data(self, payload, with_query_param, error_code, error_msg):
        headers = {API_KEY_QUERY_PARAM: self.config.get_user_api_token()} if with_query_param else {}
        res = self.client_fixture.post("/smart-tests-analyze-dev",
                                       json=payload,
                                       content_type='application/json',
                                       headers=headers)
        self.assertEqual(error_code, res.status_code)
        self.assertEqual(res.json['error_message'], error_msg)

TEST_NAMES_KEY = "test_names"
SERVICES_KEY = "services"
OLD_VERSION_KEY = "old_version"
NEW_VERSION_KEY = "new_version"
ENTRIES_KEY = "entries"
TR = "tr"
TD = "td"
B = "b"
NEXUS_URL = "http://illin5589:28080"
HELM_INDEX_REPOSITORY = "ms-helm-release"
HELM_INDEX_URL = f"{NEXUS_URL}/repository/{HELM_INDEX_REPOSITORY}/index.yaml"
GREEN_INDEX_REPOSITORY = "ms-helm-release"
GREEN_INDEX_URL = f"{NEXUS_URL}/repository/{GREEN_INDEX_REPOSITORY}/index.yaml"
NEXUS_USER = "psmdocker"
NEXUS_PASS = "unix11"
FILTERED_MS_LIST = [
    "productconfigurator",
    "productconfigurator-action",
    "productconfigurator-commitmentterm",
    "productconfigurator-mergeentities",
    "productconfigurator-pioperations",
    "productconfigurator-price",
    "productconfigurator-promotion",
    "productconfigurator-qualification",
    "productconfigurator-replace",
    "productvalidator"
]
MS_POSTFIX = "-ms"
SUPPORTED_GROUPS = ["oc-cd-group4-coc-include-ed"]
GROUP4_XML = [
    "group4_integration_tests_testng",
    "mat_APIGW_testng",
    "extended_mat_7a_APIGW_testng",
    "extended_mat_7b_APIGW_testng",
    "extended_mat_APIGW_testng",
    "shared_regression_testng",
    "grp4_integration_to_CT_testng",
    "ContratedOffer_tests_testng",
    "ContratedOffer_Pack_testng",
    "Everest_Configurator_Pack_testng",
    "Everest_Qualification_Pack_testng",
    "Everest_validator_pack",
    "Olympus_pack_testng",
]

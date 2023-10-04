import os.path

import requests

from constants.constants import MS_POSTFIX, TEST_BLOCK_PLACE_HOLDER, TEST_NAME_PLACE_HOLDER, TEST_PATH_PLACE_HOLDER
from exceptions.emptyInputError import EmptyInputError
from exceptions.notFoundError import NotFoundError


class SmartTestsClient:

    def analyze_flows(self,
                      services_map: dict,
                      filter_for_curr_group: list[str],
                      test_names_by_group: dict):
        flows_by_group = self.__get_flows(services_map, filter_for_curr_group)
        if flows_by_group is not None:
            for group in flows_by_group:
                if group in test_names_by_group:
                    test_names_by_group[group].extend(
                        [flow for flow in flows_by_group[group] if flow not in test_names_by_group[group]])
                else:
                    test_names_by_group[group] = flows_by_group[group]
        else:
            raise NotFoundError("Failed to find flows to run")

    def create_testng_xml(self, flows: list, group_name: str, group_filter: str):
        if len(flows) > 0:
            flows_block = ""
            for flow in flows:
                curr_block = self.__create_test_block(flow)
                if curr_block is not None:
                    flows_block = f"{flows_block}\n{curr_block}\n"

            template_name = group_name.replace(".xml", "").strip()
            with open(f"templates/{group_filter}/{template_name}.txt", mode="r") as file:
                template = file.read()

            flows_block = flows_block if flows_block else ""
            template = template.replace(TEST_BLOCK_PLACE_HOLDER, flows_block.strip())

            path_dir = "testNG"
            is_exist = os.path.exists(path_dir)
            if not is_exist:
                os.makedirs(path_dir)

            if ".xml" not in group_name:
                group_name = f"{group_name}.xml"

            with open(f"{path_dir}/{group_name}", mode="w") as file:
                file.write(template)
        else:
            raise EmptyInputError("no flows provided to create testng xml")

    def get_all_flows_by_filter(self, include_filter_list: list):
        body = []
        include_filter = self.__create_filter_by_list(include_filter_list)
        if include_filter:
            body.append({
                "includeFileGroupNamePattern": include_filter
            })

        with requests.post(url="https://amd-apigw-stack-service-oc-cd-ml-devops-light-tracer.apps.ilocpde529.ocpd.corp"
                               ".amdocs.com/lightTracer/v1/smart-tests-all",
                           json=body,
                           verify=False) as res:
            res.raise_for_status()
            data = res.json()

        flows_res = {"total_count": data["flowsCount"]}
        flows_per_xml = {}
        for curr_xml in data["smartTestsAllItem"]:
            name = curr_xml["name"].split("/")[-1]
            flows_per_xml[name] = {
                "count": curr_xml["flowsCount"],
                "flows": curr_xml["flows"],
            }

        flows_res["groups"] = flows_per_xml
        return flows_res

    def __get_flows(self, services_map, filter_group):
        if services_map is not None:
            flows_by_group = {}
            for service_key in services_map:
                if services_map[service_key]["old_version"] == services_map[service_key]["new_version"]:
                    continue

                body = [
                    {
                        "infoLevel": "info",
                        "restrictions": [
                            "repo_exclude_config"
                        ],
                        "project": "DIGOC",
                        "repo": f"{service_key}{MS_POSTFIX}",
                        "to": services_map[service_key]["old_version"],
                        "from": services_map[service_key]["new_version"],
                        "includeFileGroupNamePattern": self.__create_filter_by_list(filter_group)
                    }
                ]

                with requests.post(
                        url="https://amd-apigw-stack-service-oc-cd-ml-devops-light-tracer.apps.ilocpde529.ocpd.corp"
                            ".amdocs.com/lightTracer/v1/smart-tests-statistics",
                        params={"queryType": "repo"},
                        json=body,
                        verify=False) as res:
                    res.raise_for_status()
                    res_json = res.json()

                if int(res_json["flowsCount"]) > 0:
                    groups = res_json["flowsByGroupName"]
                    for group in groups:
                        group_name = group["name"].split("/")[-1]
                        if group_name in flows_by_group:
                            full_tests = [test for test in group["flows"] if test not in flows_by_group[group_name]]
                            flows_by_group[group_name].extend(full_tests)
                        else:
                            flows_by_group[group_name] = group["flows"]

            return flows_by_group
        else:
            raise EmptyInputError("failed to fetch flows to analyze. no services found.")

    def __create_test_block(self, flow_path: str):
        flow_name = flow_path.split(".")[-1]
        with open("templates/testBlockTemplate.txt", mode="r") as file:
            template = file.read()

        template = template.replace(TEST_NAME_PLACE_HOLDER, flow_name)
        template = template.replace(TEST_PATH_PLACE_HOLDER, flow_path)
        return template

    def __create_filter_by_list(self, values: list):
        if values is None or len(values) == 0:
            return ""

        values = [f".*{value}.*" for value in values]
        return "|".join(values)

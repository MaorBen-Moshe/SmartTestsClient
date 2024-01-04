# Flask API for Smart Tests Analysis

This is a flask application that provides several endpoints for analyzing the test flows to run based on the changes in the services versions.

## Installation

To install the required dependencies, run the following command:

`pip install -r requirements.txt`

## Usage

The application exposes three endpoints:

### /supported-groups

This endpoint is a GET method and returns in the response all the supported groups the server supports.

**Response example:**

```json
{
    "oc-cd-group4": {
        "cluster": "ilocpde456",
        "group_name": "oc-cd-group4",
        "project": "DIGOC",
        "url": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/",
        "ms_list": ["productconfigurator", "productconfigurator-pioperations"],
        "test_files": ["ContratedOffer_Pack_testng.xml"]
    }
}
```

### /supported-services

This endpoint is a GET method and returns in the response all the supported services the server supports.

query params:
groupName: str [optional] = if provided the response will contain only the services that are part of the group.

**Response example:**

```json
[
    {
        "name": "productconfigurator",
        "project": "DIGOC",
        "repo_name": "productconfigurator-ms",
        "related_group": "oc-cd-group4"
    }
]
```


### /smart-tests-analyze

This endpoint is a POST method. It gets in the request build_url and supported group and returns in the response json that contains flows to run per testGroup.

Payload fields:

- **groupName**: str [mandatory] = one of the supported groups
- **buildUrl**: str [mandatory] = url to a zip file of the jenkins build report
- **sessionID**: str = this session id is added to message sent from the server in the socket channel namespace: /smart-analyze-progress and event name is -smart-analyze-progress.
- **infoLevel**: str = valid values: info or debug. if not provided the default value is info. this field affects on the response data. in debug we add also the services data in the response.

**Request example:**
    
```json
{
    "groupName": "oc-cd-group4",
    "buildUrl": "http://illin5565:18080/job/oc-cd-group4/job/oc-cd-group4/lastSuccessfulBuild/artifact/oc-cd-group4.zip",
    "sessionID": "1234",
    "infoLevel": "info"
}
```

**Response example:**
```json
{
  "curr_flows_count": 2,
  "groups": {
    "ContratedOffer_Pack_testng.xml": {
      "curr_flows_count": 2,
      "flows": [
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS_71143_reject_unReject_promotion",
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS70993_ManageManualPromotion_AddPromotionToContractedInstance"
      ],
      "test_xml_name": "ContratedOffer_Pack_testng.xml",
      "test_xml_path": "com/amdocs/core/oc/group4/testng",
      "total_flows_count": 24
    }
  },
  "total_flows_count": 24
}
```

### /smart-tests-analyze-dev
This endpoint is a POST method. It gets in the request services list and for each service makes the analysis of flows to run because of the changes in the version.

Payload fields:

- **services**: list[object] = each service is object contains service data input. the object can contain the following fields:
    - **name**: str [mandatory] = service name
    - **from**: str [optional] = service from version
    - **to**: str [optional] = service to version
    - **pullRequestId**: str [optional] = pull request id. if provided the from and to fields are ignored and the service versions are taken from the pull request commits. 
- **sessionID**: str = this session id is added to message sent from the server in the socket channel namespace: /smart-analyze-progress and event name is -smart-analyze-progress.
- **infoLevel**: str = valid values: info or debug. if not provided the default value is info. this field affects on the response data. in debug, we add also the services data in the response.

**Request example**:
```json
{
    "services": [
        {
            "name": "productconfigurator",
            "from": "0.67.110",
            "to": "0.67.109"
        },
        {
            "name": "productconfigurator-commitmentterm",
            "from": "0.67.100"
        },
        {
            "name": "productconfigurator-pioperations",
            "pullRequestId": "12345"
        }
    ],
    "sessionID": "1234",
    "infoLevel": "debug"
}
```

**Response example**:

```json
{
  "curr_flows_count": 2,
  "groups": {
    "ContratedOffer_Pack_testng.xml": {
      "curr_flows_count": 2,
      "flows": [
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS_71143_reject_unReject_promotion",
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS70993_ManageManualPromotion_AddPromotionToContractedInstance"
      ],
      "test_xml_name": "ContratedOffer_Pack_testng.xml",
      "test_xml_path": "com/amdocs/core/oc/group4/testng",
      "total_flows_count": 24
    }
  },
  "services": {
    "productconfigurator": {
      "flows": [],
      "from": "0.67.110",
      "to": "0.67.109"
    },
    "productconfigurator-commitmentterm": {
      "flows": [
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS_71143_reject_unReject_promotion",
        "com.amdocs.core.oc.group4.test.flows.contractedOffer.CROSS70993_ManageManualPromotion_AddPromotionToContractedInstance"
      ],
      "from": "0.67.100",
      "to": "0.67.94"
    },
    "productconfigurator-pioperations": {
      "flows": [],
      "pullRequestId": "12345"
    }
  },
  "total_flows_count": 24
}
```


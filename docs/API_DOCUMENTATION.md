# MCP Data API Documentation

## Overview

This document provides comprehensive API documentation for the MCP Data API service. The service provides access to category management, API discovery, API execution, and SQL query capabilities.

## Base Configuration

All requests require the following headers:
- `app_id`: Application identifier (e.g., "984")
- `dbName`: Database name (e.g., "hc_data_center")

## API Endpoints

### 1. Get Category List

Retrieves a hierarchical list of API categories.

**Endpoint:** `GET /file/directory`

**Service:** chatgpt-api-service

**Base URL:** `http://chatgpt-api-service:31001`

#### Request Parameters

| Parameter | Type   | Required | Description                    |
|-----------|--------|----------|--------------------------------|
| appId     | string | Yes      | Application identifier         |
| source    | string | No       | Source type (default: "API")   |

#### Response

**Success Response (200 OK)**

```json
{
    "data": [
        {
            "id": 19776,
            "name": "测试API",
            "parentId": null,
            "children": [
                {
                    "id": 19992,
                    "name": "测试子级",
                    "parentId": 19776,
                    "children": null
                }
            ]
        }
    ],
    "message": {
        "code": 0,
        "detail": null,
        "message": "success",
        "status": 200
    }
}
```

#### Response Fields

| Field                | Type    | Description                           |
|----------------------|---------|---------------------------------------|
| data                 | array   | Array of category objects             |
| data[].id            | integer | Category unique identifier            |
| data[].name          | string  | Category name                         |
| data[].parentId      | integer | Parent category ID (null for root)    |
| data[].children      | array   | Nested child categories               |
| message.code         | integer | Response code (0 for success)         |
| message.message      | string  | Response message                      |
| message.status       | integer | HTTP status code                      |

#### Notes

- Child categories should be flattened with parent names concatenated using ">" separator
- Example: "测试API>测试子级"
- Process the response into Category objects

#### Example Request

```bash
curl --location --request GET 'http://chatgpt-api-service:31001/file/directory?appId=984&source=API'
```

---

### 2. Get API List by Category

Retrieves a list of APIs belonging to a specific category.

**Endpoint:** `GET /agent/queryByNames`

**Service:** chatdb-visual-service

**Base URL:** `http://chatdb-visual-service:31001`

#### Request Parameters

| Parameter | Type    | Required | Description                    |
|-----------|---------|----------|--------------------------------|
| appId     | string  | Yes      | Application identifier         |
| treeId    | integer | Yes      | Category ID from Category object |

#### Response

**Success Response (200 OK)**

```json
{
    "data": [
        {
            "appId": "984",
            "description": "接口描述",
            "id": 971,
            "method": "GET",
            "name": "资金分类看板",
            "queryParams": [
                {
                    "afterHandle": "",
                    "content": "10135",
                    "desc": "",
                    "isNecessary": "否",
                    "name": "port",
                    "parentIndex": "",
                    "type": ""
                }
            ],
            "queryType": "formData",
            "url": "http://localhost:8080"
        }
    ],
    "message": {
        "code": 0,
        "detail": null,
        "message": "success",
        "status": 200
    }
}
```

#### Response Fields

| Field                      | Type    | Description                           |
|----------------------------|---------|---------------------------------------|
| data                       | array   | Array of API objects                  |
| data[].appId               | string  | Application identifier                |
| data[].description         | string  | API description                       |
| data[].id                  | integer | API unique identifier                 |
| data[].method              | string  | HTTP method (GET, POST, etc.)         |
| data[].name                | string  | API name                              |
| data[].queryParams         | array   | Query parameters configuration        |
| data[].queryType           | string  | Query type (formData, json, etc.)     |
| data[].url                 | string  | API endpoint URL                      |

#### Notes

- Process the data array into APIBasic objects

#### Example Request

```bash
curl --location --request GET 'http://chatdb-visual-service:31001/agent/queryByNames?appId=984&treeId=1640'
```

---

### 3. Get API Details by Names

Retrieves detailed information for one or more APIs by their names.

**Endpoint:** `GET /agent/queryByNames`

**Service:** chatdb-visual-service

**Base URL:** `http://chatdb-visual-service:31001`

#### Request Parameters

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| appId     | string | Yes      | Application identifier                   |
| names     | string | Yes      | Comma-separated list of API names        |

#### Response

**Success Response (200 OK)**

```json
{
    "data": [
        {
            "appId": "984",
            "description": "接口描述",
            "id": 971,
            "method": "GET",
            "name": "资金分类看板",
            "queryParams": [
                {
                    "afterHandle": "",
                    "content": "10135",
                    "desc": "",
                    "isNecessary": "否",
                    "name": "port",
                    "parentIndex": "",
                    "type": ""
                }
            ],
            "queryType": "formData",
            "url": "http://localhost:8080"
        }
    ],
    "message": {
        "code": 0,
        "detail": null,
        "message": "success",
        "status": 200
    }
}
```

#### Query Parameters Field Explanation

| Field        | Description                                    |
|--------------|------------------------------------------------|
| name         | Parameter name                                 |
| type         | Parameter type (default: string)               |
| content      | Default value                                  |
| isNecessary  | Whether parameter is required ("是" or "否")   |
| desc         | Parameter description                          |

#### Example Request

```bash
curl --location --request GET 'http://chatdb-visual-service:31001/agent/queryByNames?appId=984&names=资金分类看板,oa发票关键字分页查询,自营持仓交易资金关联'
```

---

### 4. Execute API

Executes a single API with provided parameters.

**Endpoint:** `POST /dataApiInfo/callApi`

**Service:** chatdb-visual-service

**Base URL:** `http://chatdb-visual-service:31001`

#### Request Headers

| Header       | Value              | Required |
|--------------|-------------------|----------|
| Content-Type | application/json  | Yes      |

#### Request Body

| Field    | Type   | Required | Description                           |
|----------|--------|----------|---------------------------------------|
| appId    | string | Yes      | Application identifier                |
| apiName  | string | Yes      | Name of the API to execute            |
| reqMap   | object | Yes      | Request parameters as JSON object     |

#### Request Example

```json
{
    "apiName": "费控结算单关键字分页查询",
    "appId": "984",
    "reqMap": {
        "ids": "1001D210000000016SJE",
        "dbId": "hc_data_center",
        "keyword": "差旅",
        "bankRelatedCode": "004SUV"
    }
}
```

#### Notes

- This endpoint can only execute one API at a time
- For multiple API executions, the caller must handle multiple requests

#### Example Request

```bash
curl --location --request POST 'http://chatdb-visual-service:31001/dataApiInfo/callApi' \
--header 'Content-Type: application/json' \
--data-raw '{
    "apiName": "费控结算单关键字分页查询",
    "appId": "984",
    "reqMap": {
        "ids": "1001D210000000016SJE",
        "dbId": "hc_data_center",
        "keyword": "差旅",
        "bankRelatedCode": "004SUV"
    }
}'
```

---

### 5. Execute SQL Query

Executes a SQL query against the specified database.

**Endpoint:** `POST /sqlQuery/execSql`

**Service:** llm-workflow-service

**Base URL:** `http://llm-workflow-service:31001`

#### Request Headers

| Header       | Value              | Required |
|--------------|-------------------|----------|
| Content-Type | application/json  | Yes      |

#### Request Body

| Field      | Type   | Required | Description                              |
|------------|--------|----------|------------------------------------------|
| appId      | string | Yes      | Application identifier                   |
| sql        | string | Yes      | SQL query to execute                     |
| sourceName | string | Yes      | Database source name (from dbName header)|

#### Request Example

```json
{
    "appId": "984",
    "sql": "SELECT SUM(vat_amount) AS total_meal_cost FROM er_busitem_other WHERE jkbxr_detail = '屈庆' AND YEAR(startdate) = 2025;",
    "sourceName": "数据中台"
}
```

#### Response

**Success Response (200 OK)**

```json
{
    "data": [
        {
            "total_meal_cost": 7340.72000000
        },
        {
            "name": "output_standard_chart",
            "type": "dict",
            "value": [
                {
                    "total_meal_cost": 7340.72000000
                }
            ],
            "multiline": true
        },
        {
            "name": "output_json_schema",
            "type": "dict",
            "value": [
                {
                    "name": "total_meal_cost",
                    "type": "Number"
                }
            ],
            "multiline": true
        }
    ],
    "message": {
        "code": 0,
        "detail": null,
        "message": "success",
        "status": 200
    }
}
```

#### Response Fields

| Field                           | Type    | Description                           |
|---------------------------------|---------|---------------------------------------|
| data                            | array   | Array containing query results        |
| data[0]                         | object  | Direct query result                   |
| data[1].name                    | string  | Output type identifier                |
| data[1].value                   | array   | Standardized chart data               |
| data[2].value                   | array   | JSON schema of result columns         |

#### Notes

- Focus on the `output_standard_chart` value field for the standardized result
- The first element in data array contains the raw query result
- Return the value from `output_standard_chart` to the agent

#### Example Request

```bash
curl --location --request POST 'http://llm-workflow-service:31001/sqlQuery/execSql' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "984",
    "sql": "SELECT SUM(vat_amount) AS total_meal_cost FROM er_busitem_other WHERE jkbxr_detail = '\''屈庆'\'' AND YEAR(startdate) = 2025;",
    "sourceName": "数据中台"
}'
```

---

## Error Handling

All endpoints return a standard error response format:

```json
{
    "data": null,
    "message": {
        "code": <error_code>,
        "detail": "<error_details>",
        "message": "<error_message>",
        "status": <http_status_code>
    }
}
```

### Common Error Codes

| Status Code | Description                    |
|-------------|--------------------------------|
| 200         | Success                        |
| 400         | Bad Request                    |
| 401         | Unauthorized                   |
| 404         | Not Found                      |
| 500         | Internal Server Error          |

---

## Data Models

### Category Object

```typescript
interface Category {
    id: number;
    name: string;
    parentId: number | null;
    children: Category[] | null;
}
```

### APIBasic Object

```typescript
interface APIBasic {
    appId: string;
    description: string;
    id: number;
    method: string;
    name: string;
    queryParams: QueryParam[];
    queryType: string;
    url: string;
}
```

### QueryParam Object

```typescript
interface QueryParam {
    name: string;
    type: string;
    content: string;
    isNecessary: string;
    desc: string;
    afterHandle: string;
    parentIndex: string;
}
```

---

## Version History

| Version | Date       | Changes                          |
|---------|------------|----------------------------------|
| 1.0.0   | 2026-02-05 | Initial API documentation        |

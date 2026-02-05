
## 请求案例：

curl --location --request POST 'http://llm-workflow-service:31001/sqlQuery/execSql' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "984",
    "sql": "SELECT SUM(vat_amount) AS total_meal_cost FROM er_busitem_other WHERE jkbxr_detail = '\''屈庆'\'' AND YEAR(startdate) = 2025;",
    "sourceName": "数据中台"
}'

## 请求参数
1. appId 变量
2. sql 
3. sourceName 来自于 header中的 dbName 

## 返回案例
关注 output_standard_chart中的value 的内容 返回给 agent 
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
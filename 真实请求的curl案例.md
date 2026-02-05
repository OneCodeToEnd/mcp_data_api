## 获取分类列表

服务:chatgpt-api-service
接口地址:curl --location --request GET 'http://chatgpt-api-service:31001/file/directory?appId=984&source=API'

请求参数:
1. appId 变量
2. source默认是 source 

响应参数(格式 json)
1. 样例:
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

注意事项: 
你需要把子级children 打平，提到父级名称更改为 测试API>测试子级
加工成Category对象返回即可

## 根据分类获取 API 列表

服务:chatdb-visual-service
接口地址:curl --location --request GET 'http://chatdb-visual-service:31001/agent/queryByNames?appId=984&treeId=1640'
请求参数:
1. appId 变量
2. treeId 为 Category对象 的 id 

响应参数(格式 json)
案例:
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
注意事项：
将 data 中的内容加工成 APIBasic 即可


## 根据 API 列表获取 API 详情


服务:chatdb-visual-service
接口地址:curl --location --request GET 'http://chatdb-visual-service:31001/agent/queryByNames?appId=984&names=资金分类看板,oa发票关键字分页查询,自营持仓交易资金关联'
请求参数:
1. appId 变量
2. names 为用户传递的 api 名称

响应参数(格式 json)
案例:
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
关键：
queryParams字段解释
1. name:字段名称
2. type:类型默认字符串
3. content: 默认值
4. isNecessary:是否必传

## 执行多个API

服务:chatdb-visual-service
接口地址（接口只能执行一个 1 个 api,如果执行多个需要调用侧处理）:
```shell
curl --location --request POST 'http://chatdb-visual-service:31001/dataApiInfo/callApi' \
--header 'Content-Type: application/json' \
--data-raw '{
    "apiName": "费控结算单关键字分页查询",
    "appId": "984",
    "reqMap": {
        "ids": "1001D210000000016SJE",
        "dbId": "hc_data_center",
        "keyword":"差旅",
        "bankRelatedCode":"004SUV"
    }
}'
```
请求参数:
1. appId 变量
2. apiName api名称
3. reqMap 请求参数，json 格式


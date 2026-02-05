import json

original_json = '''
{
    "data": [
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276507439,
            "dataSource": "QDoc",
            "description": "",
            "id": 17462,
            "name": "后端API",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276507439,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276507558,
            "dataSource": "QDoc",
            "description": "",
            "id": 17464,
            "name": "数据同步",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276507558,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276507605,
            "dataSource": "QDoc",
            "description": "",
            "id": 17466,
            "name": "信用业务",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276507605,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276507736,
            "dataSource": "QDoc",
            "description": "",
            "id": 17468,
            "name": "银行流水",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276507736,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276508899,
            "dataSource": "QDoc",
            "description": "",
            "id": 17470,
            "name": "费控业务",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276508899,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1765276509765,
            "dataSource": "QDoc",
            "description": "",
            "id": 17472,
            "name": "tp测试",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1765276509765,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1769657111819,
            "dataSource": "QDoc",
            "description": "",
            "id": 19770,
            "name": "同业拆借",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1769657111819,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1769657112112,
            "dataSource": "QDoc",
            "description": "",
            "id": 19772,
            "name": "回购",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1769657112112,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1769657112268,
            "dataSource": "QDoc",
            "description": "",
            "id": 19774,
            "name": "任务消息模块",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1769657112268,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": [
                {
                    "actionUserGroupId": null,
                    "actionUserId": null,
                    "appId": 3010,
                    "channel": "rxhui",
                    "children": null,
                    "createAt": 1770002234283,
                    "dataSource": "QDoc",
                    "description": "",
                    "id": 19992,
                    "name": "测试子级",
                    "parentId": 19776,
                    "parentSourceId": null,
                    "readUserGroupId": null,
                    "readUserId": null,
                    "source": "API",
                    "sourceId": null,
                    "sourceMeta": null,
                    "status": 0,
                    "totalNumber": 0,
                    "updateAt": 1770002234283,
                    "userGroupId": "100",
                    "userId": "1",
                    "userInfo": null,
                    "userName": "admin",
                    "workflowId": 0,
                    "writeUserGroupId": null,
                    "writeUserId": null
                }
            ],
            "createAt": 1769657115242,
            "dataSource": "QDoc",
            "description": "",
            "id": 19776,
            "name": "测试API",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1769657115242,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        },
        {
            "actionUserGroupId": null,
            "actionUserId": null,
            "appId": 3010,
            "channel": "rxhui",
            "children": null,
            "createAt": 1769657115538,
            "dataSource": "QDoc",
            "description": "",
            "id": 19778,
            "name": "对手方交易详情",
            "parentId": null,
            "parentSourceId": null,
            "readUserGroupId": null,
            "readUserId": null,
            "source": "API",
            "sourceId": null,
            "sourceMeta": null,
            "status": 0,
            "totalNumber": 0,
            "updateAt": 1769657115538,
            "userGroupId": "100",
            "userId": "1",
            "userInfo": null,
            "userName": "admin",
            "workflowId": 0,
            "writeUserGroupId": null,
            "writeUserId": null
        }
    ],
    "message": {
        "code": 0,
        "detail": null,
        "message": "success",
        "status": 200
    }
}
'''

# 定义需要保留的字段（不变）
keep_fields = ["id", "name", "parentId", "children"]


def filter_json_item(item):
    """
    递归过滤单个JSON对象，兼容多层children嵌套
    无论是顶层对象还是children中的嵌套对象，都只保留指定4个字段
    """
    if not isinstance(item, dict):
        return item

    # 初始化过滤后的对象
    filtered_item = {}
    for field in keep_fields:
        if field in item:
            value = item[field]
            # 处理数组类型（children是数组时，遍历每个子元素递归过滤）
            if isinstance(value, list):
                filtered_item[field] = [filter_json_item(sub_item) for sub_item in value]
            # 处理嵌套对象类型（如果children是单个对象，递归过滤）
            elif isinstance(value, dict):
                filtered_item[field] = filter_json_item(value)
            # 普通类型（null、数字、字符串）直接保留
            else:
                filtered_item[field] = value

    return filtered_item


# 1. 解析原始JSON为Python字典
data_dict = json.loads(original_json)

# 2. 过滤data数组中的每个元素（包含嵌套children的递归过滤）
if "data" in data_dict and isinstance(data_dict["data"], list):
    data_dict["data"] = [filter_json_item(item) for item in data_dict["data"]]

# 3. 转换回格式化后的JSON字符串（保留中文，缩进4格）
filtered_json = json.dumps(data_dict, ensure_ascii=False, indent=4)

# 4. 输出结果
print("过滤后的JSON结果（含正确嵌套的children）：")
print(filtered_json)
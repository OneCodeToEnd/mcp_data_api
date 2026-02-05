import json
import re


original_json = '''
{
    "appId": "3010",
    "desc": "InvoiceInfoByKeyWord",
    "name": "oa发票关键字分页查询",
    "queryArr": [
        {
            "afterHandle": "",
            "content": "829",
            "desc": "",
            "isNecessary": "否",
            "name": "dbId",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "1",
            "desc": "",
            "isNecessary": "否",
            "name": "cp",
            "parentIndex": "",
            "type": "NUMBER"
        },
        {
            "afterHandle": "",
            "content": "10",
            "desc": "",
            "isNecessary": "否",
            "name": "ps",
            "parentIndex": "",
            "type": "NUMBER"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "",
            "isNecessary": "否",
            "name": "keyword",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "账号",
            "isNecessary": "否",
            "name": "accountNumber",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "开户行",
            "isNecessary": "否",
            "name": "bankName",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "金额",
            "isNecessary": "否",
            "name": "amt",
            "parentIndex": "",
            "type": "NUMBER"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "排除ids 列表",
            "isNecessary": "否",
            "name": "excludeIds",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "yyyyMMdd开票日期范围",
            "isNecessary": "否",
            "name": "dataDateStart",
            "parentIndex": "",
            "type": "STRING"
        },
        {
            "afterHandle": "",
            "content": "",
            "desc": "yyyyMMdd开票日期范围",
            "isNecessary": "否",
            "name": "dataDateEnd",
            "parentIndex": "",
            "type": "STRING"
        }
    ],
    "treeId": "17462"
}
'''

# 定义需要保留的字段（不变）
keep_fields = ["id", "name", "desc", "treeId"]


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


def preprocess_json_string(json_str):
    """
    预处理JSON字符串：删除包含非法字符的大字段（如 glueSource, queryArr, returnArr）
    这样可以避免解析时的控制字符错误，同时大幅减少解析体积。
    """
    # 定义需要删除的字段名列表
    fields_to_remove = [
        'glueSource',
        'queryArr',
        'returnArr',
        'headerArr',
        'queryStr',
        'returnOriginStr',
        'returnStr'
    ]

    processed_str = json_str
    for field in fields_to_remove:
        # 构建正则模式，匹配字段名及其对应的值
        # 模式解释：
        # "field_name"      匹配字段名
        # \s*:\s*            匹配冒号及周围可能的空格
        # (?:                开始非捕获组
        #   "[^"\\]*(?:\\.[^"\\]*)*"  匹配双引号字符串（处理转义字符）
        #   |                 或者
        #   \[[^\]]*\]       匹配中括号数组（非贪婪匹配直到遇到对应的 ]）
        #   |                 或者
        #   [^,\[\]{}]+      匹配非数组、非对象、非逗号的简单值（如数字, true, false, null）
        # )                  结束非捕获组
        pattern = re.compile(r'"' + re.escape(field) + r'"\s*:\s*(?:"[^"\\]*(?:\\.[^"\\]*)*"|\[[^\]]*\]|[^,\[\]{}]+)')

        # 将匹配到的字段及其值替换为空字符串
        # 注意：这里简单替换可能会导致残留逗号，但 Python json.loads 通常能容忍对象末尾的逗号或连续逗号（需视具体版本而定）
        # 更稳健的做法是替换为 null 或空字符串/空数组
        processed_str = pattern.sub('"' + field + '": null', processed_str)

    return processed_str


# 1. 预处理 JSON 字符串，移除包含代码的大字段
try:
    cleaned_json_str = preprocess_json_string(original_json)
except Exception as e:
    print(f"预处理失败: {e}")
    exit(1)

# 2. 解析清洗后的 JSON
try:
    data_dict = json.loads(cleaned_json_str)
except json.JSONDecodeError as e:
    # 如果还是失败，打印错误位置附近的字符以便调试
    print(f"JSON解析错误: {e}")
    error_pos = e.pos
    print(f"错误位置附近内容: ...{cleaned_json_str[max(0, error_pos - 50):error_pos + 50]}...")
    exit(1)

# 2. 过滤data数组中的每个元素（包含嵌套children的递归过滤）
if "data" in data_dict and isinstance(data_dict["data"], dict):
    if "rows" in data_dict["data"] and isinstance(data_dict["data"]["rows"], list):
        data_dict["data"]["rows"] = [filter_json_item(item) for item in data_dict["data"]["rows"] ]

# 3. 转换回格式化后的JSON字符串（保留中文，缩进4格）
filtered_json = json.dumps(data_dict, ensure_ascii=False, indent=4)

# 4. 输出结果
print("过滤后的JSON结果（含正确嵌套的children）：")
print(filtered_json)
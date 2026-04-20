import pandas as pd


def convert_counts_to_pie_data(counts_series, value_key='value', name_key='name'):
    """
    将 pandas value_counts() 的结果转换为前端图表所需的字典列表格式。

    参数:
    counts_series: pandas Series (由 df[col].value_counts() 生成)
    value_key:   输出字典中代表数值的键名，默认为 'value'
    name_key:    输出字典中代表名称的键名，默认为 'name'

    返回:
    list: 包含字典的列表，例如 [{'name': 'A', 'value': 10}, ...]
    """
    # 方法 A: 使用列表推导式 (最直观)
    data = [
        {name_key: str(index), value_key: int(val)}
        for index, val in counts_series.items()
    ]
    return data


# --- 使用示例 ---

# 1. 模拟数据
data = {'fruit': ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']}
df = pd.DataFrame(data)

# 2. 计算计数
counts = df['fruit'].value_counts()
# counts 内容大致为:
# apple     3
# banana    2
# orange    1

# 3. 调用转换方法
result = convert_counts_to_chart_data(counts)

# 4. 打印结果
print(result)

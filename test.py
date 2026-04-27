import pandas as pd


def df_to_chart_format(df, name_col, value_col, agg_func='sum'):
    """
    将 DataFrame 转换为 [{name: '...', value: ...}] 格式

    参数:
    df: 输入的 DataFrame
    name_col: 作为 'name' 的列名 (例如: '指标名称')
    value_col: 作为 'value' 的列名 (例如: '数值')
    agg_func: 聚合方式，默认为 'sum'，也可以是 'mean', 'count' 等
    """
    # 1. 分组并聚合
    # 结果是一个 Series，索引是 name_col，值是聚合后的 value_col
    grouped = df.groupby(name_col)[value_col].agg(agg_func)

    # 2. 重置索引，变回 DataFrame，并重命名列以匹配目标格式
    result_df = grouped.reset_index()
    result_df.columns = ['name', 'value']

    # 3. 转换为字典列表
    # orient='records' 会将每一行转换为一个字典
    result_list = result_df.to_dict(orient='records')

    return result_list


# --- 测试代码 ---
# 假设这是你的原始数据
data = {
    '指标': ['CPU 核心组 A', '内存占用', 'CPU 核心组 A', '网络下行', '内存占用', '网络下行'],
    '数值': [40, 30, 45, 20, 32, 28]
}
df = pd.DataFrame(data)

# 调用方法
output = df_to_chart_format(df, '指标', '数值')

print(output)
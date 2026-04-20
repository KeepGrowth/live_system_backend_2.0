# 项目生成级联选项
import random

import pandas as pd
import redis
from pandas import DataFrame

r = redis.Redis(host='192.168.1.86', port=6379, db=0, decode_responses=True, password='redis_erHFmZ')


# 项目生成级联选项
def convert_to_year_program_options(data):
    """
    项目层级数据表工具
    生成「年份→项目(ID+名称)」的级联选项
    :param data: 原始项目列表
    :return: 级联选择器options格式
    """
    # 第一步：按创建时间的年份分组
    year_groups = {}
    for item in data:
        # 提取年份
        year = str(item['estimate_finish_time']).split('-')[0]
        # 初始化年份分组
        if year not in year_groups:
            year_groups[year] = {
                'value': str(year),  # 一级value：年份
                'label': f'{year}年',  # 一级label：XX年
                'children': []  # 二级：该年份下的项目
            }
        # 第二步：添加项目到对应年份（仅保留ID和名称）
        year_groups[year]['children'].append({
            'value': int(item['id']),  # 二级value：项目ID
            'label': item['program_name']  # 二级label：项目名称
        })

    # 转换为列表并按年份排序（可选）
    options = sorted(year_groups.values(), key=lambda x: x['value'])
    return options


# 目标生成级联选项
def convert_to_year_goal_options(data):
    """
    层级数据表工具
    生成「年份→项目(ID+名称)」的级联选项
    :param data: 原始项目列表
    :return: 级联选择器options格式
    """
    # 第一步：按创建时间的年份分组
    year_groups = {}
    for item in data:
        # 提取年份
        year = str(item['finish_date']).split('-')[0]
        # 初始化年份分组
        if year not in year_groups:
            year_groups[year] = {
                'value': year,  # 一级value：年份
                'label': f'{year}年',  # 一级label：XX年
                'children': []  # 二级：该年份下的项目
            }
        # 第二步：添加项目到对应年份（仅保留ID和名称）
        year_groups[year]['children'].append({
            'value': int(item['id']),  # 二级value：项目ID
            'label': item['goal_name']  # 二级label：项目名称
        })

    # 转换为列表并按年份排序（可选）
    options = sorted(year_groups.values(), key=lambda x: x['value'])
    return options


# 获取OKR级联选项
def convert_to_year_okr_options(data):
    """
    层级数据表工具
    生成「年份→项目(ID+名称)」的级联选项
    :param data: 原始项目列表
    :return: 级联选择器options格式
    """
    # 第一步：按创建时间的年份分组
    year_groups = {}
    for item in data:
        # 提取年份
        print("11111", type(item['create_time']))
        print(item['create_time'])
        year = str(item['create_time']).split('-')[0]
        # 初始化年份分组
        if year not in year_groups:
            year_groups[year] = {
                'value': year,  # 一级value：年份
                'label': f'{year}年',  # 一级label：XX年
                'children': []  # 二级：该年份下的项目
            }
        # 第二步：添加项目到对应年份（仅保留ID和名称）
        year_groups[year]['children'].append({
            'value': int(item['id']),  # 二级value:okrId
            'label': item['kr_name']  # 二级label：项目名称
        })

    # 转换为列表并按年份排序（可选）
    options = sorted(year_groups.values(), key=lambda x: x['value'])
    return options


# 统计某个实体记录的完成率
def calculate_completion_rate(df: DataFrame, column_name: str = 'status', target_value: int = 2):
    """
    计算指定字段中特定值的完成率（该值出现次数 / 总记录数）

    参数:
        df (pd.DataFrame): 输入的数据框
        column_name (str): 要统计的字段名
        target_value: 要统计的目标值（可以是字符串、数字等）

    返回:
        float: 完成率（0 到 1 之间的浮点数）
    """
    if column_name not in df.columns:
        raise ValueError(f"列名 '{column_name}' 不存在于数据框中")

    total_records = len(df)
    if total_records == 0:
        return 0.0

    target_count = (df[column_name] == target_value).sum()
    completion_rate = target_count / total_records

    return completion_rate


# 统计某个字段值的计数。
def count_by_column(df, column_name):
    """
    根据指定字段进行分组并计算每个值的计数

    参数:
        df (pd.DataFrame): 输入的DataFrame
        column_name (str): 要进行分组计算的字段名称

    返回:
        pd.Series: 每个值对应的计数
    """
    # 检查字段是否存在
    if column_name not in df.columns:
        raise ValueError(f"字段 '{column_name}' 不存在于DataFrame中")

    # 使用value_counts()方法计算每个值的计数
    counts = df[column_name].value_counts()
    print('3333', counts)
    return counts


# 将dataframe转为堆叠条形图的数据格式
def convert_df_to_stack_chart_data(df, index_col, column_col, value_col):
    """
    将 DataFrame 转换为 ECharts 所需的 seriesList 和 categories 结构

    参数:
    df: 输入的 pandas DataFrame
    index_col: 用作 Series 名称的列名 (对应图中的 program_id)
    column_col: 用作 Categories 的列名 (对应图中的 goal_id)
    value_col: 需要聚合计算的数值列名 (对应图中的 focus_time总和)
    """

    # 1. 数据透视 (Pivot Table)
    # index: 行索引 (program_id)
    # columns: 列索引 (goal_id)
    # values: 填充值 (focus_time)
    # aggfunc: 聚合函数，防止重复数据报错，虽然你的图看起来是一对一，但加上更安全
    pivot_df = pd.pivot_table(df, index=index_col, columns=column_col, values=value_col, aggfunc='sum')

    # 2. 处理缺失值 (可选)
    # 如果某些 program 没有某个 goal 的数据，会变成 NaN，通常填充为 0
    pivot_df = pivot_df.fillna(0)

    # 3. 生成 categories (X轴)
    # pivot_df.columns 是 goal_id 的列表
    # 如果列名有层级（pivot操作有时会生成MultiIndex），需要扁平化处理，否则直接转list
    categories = pivot_df.columns.tolist()

    # 4. 生成 seriesList
    series_list = []
    cyber_colors = [
        '#00f3ff',
        '#ff00ff',
        '#fcee0a',
        '#7000ff',
        '#ff2a2a'
    ]

    # iterrows 遍历每一行，row.name 就是 program_id
    for idx, row in pivot_df.iterrows():
        series_item = {
            "name": str(idx),  # program_id 作为 series 的 name
            "data": row.values.tolist(),  # 该行的所有数值作为 data 数组
            "type": 'bar',
            'itemStyle': {
                'color': random.choice(cyber_colors),
            }
        }
        series_list.append(series_item)

    return {
        "series": series_list,
        "categories": categories
    }


# 将df转为饼图数据格式
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


# 校验验证码
def verify_code(
        code: str,
        email: str,
):
    print(email, code)
    stored_code = r.get(email)
    print(stored_code)
    # 2. 校验
    if not stored_code:
        return False

    if stored_code == code:
        # 验证成功后，立即删除验证码，防止重用
        r.delete(email)
        return True
    else:
        return False

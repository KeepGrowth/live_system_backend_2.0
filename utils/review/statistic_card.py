"""
累计指标卡计算类
"""
import pandas as pd
import numpy as np


class AccumulateStatisticCard:

    @staticmethod
    def calculate_completion_stats(df, status_col='status', completed_status_num: int = 2):
        """
        计算 DataFrame 的总记录数和完成率。

        参数:
        df (pd.DataFrame): 包含任务数据的 DataFrame。
        status_col (str): 表示任务状态的列名，默认为 'status'。

        返回:
        dict: 包含总记录数、已完成数、完成率的字典。
        """

        # 1. 获取总记录数
        total_count = len(df)

        # 如果 DataFrame 为空，直接返回 0 避免报错
        if total_count == 0:
            return {
                "total_count": 0,
                "completed_count": 0,
                "completion_rate": 0.0
            }

        # 2. 筛选状态为 2 (已完成) 的记录数--completed_status_num
        completed_count = df[df[status_col] == completed_status_num].shape[0]

        # 3. 计算完成率
        # 公式：(已完成数量 / 总数量) * 100%
        completion_rate = (completed_count / total_count) * 100

        return {
            "total_count": int(total_count),
            "completed_count": int(completed_count),
            "completion_rate": float(round(completion_rate, 2))  # 保留两位小数
        }





# --- 测试示例 ---

# 构造模拟数据
data = {
    'id': [101, 102, 103, 104, 105, 106],
    'task_name': ['写报告', '修Bug', '开会', '代码审查', '部署', '测试'],
    'status': [0, 1, 2, 2, 3, 2]  # 对应：待完成, 进行中, 已完成, 已完成, 已放弃, 已完成
}
df_test = pd.DataFrame(data)

# 调用函数
a = AccumulateStatisticCard()
result = a.calculate_completion_stats(df_test, status_col='status')

print(f"总记录数: {result['total_count']}")
print(f"已完成数: {result['completed_count']}")
print(f"完成率: {result['completion_rate']}%")

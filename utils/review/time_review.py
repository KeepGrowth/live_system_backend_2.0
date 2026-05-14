"""
时间维度复盘计算方法
"""

import pandas as pd
import numpy as np
from datetime import date, datetime


# 日复盘
def calculate_daily_metrics(todo_df: pd.DataFrame, log_df: pd.DataFrame, target_date: date) -> dict:
    """
    统计每日五个核心指标。

    参数:
    - todo_df: 对应数据库 todo表的 DataFrame
    - log_df: 对应数据库 todo_log 表的 DataFrame
    - target_date: 目标日期 (datetime.date 或 datetime.datetime)

    返回:
    - 包含五个指标结果的字典
    """

    # 1. 数据预处理：确保时间字段格式正确
    # 如果已经是 datetime 类型，这步不会报错，但确保安全
    if not np.issubdtype(todo_df['deadline'].dtype, np.datetime64):
        todo_df['deadline'] = pd.to_datetime(todo_df['deadline']).dt.date

    if not np.issubdtype(log_df['create_time'].dtype, np.datetime64):
        log_df['create_time'] = pd.to_datetime(log_df['create_time'])

    # 如果传入的是 datetime，转换为 date 以便比较
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    # 2. 筛选“今日计划”
    # 定义：deadline 为当日
    today_todos = todo_df[todo_df['deadline'] == target_date].copy()

    # 如果今天没有计划，处理空数据情况
    if today_todos.empty:
        return {
            "今日待办完成率": 0.0,
            "平均专注时长": 0.0,
            "今日情绪画像": "无数据",
            "平均满意度": 0.0,
            "中断/放弃数": 0
        }

    total_plan_count = len(today_todos)

    # 3. 计算基于 todo 表的指标

    # [指标1] 今日待办完成率
    # 逻辑：今日状态为“已完成”(2)的Todo数 / 今日计划Todo数
    completed_count = today_todos[today_todos['status'] == 2].shape[0]
    completion_rate = completed_count / total_plan_count if total_plan_count > 0 else 0

    # [指标5] 中断/放弃数
    # 逻辑：今日状态为“已放弃”(3)的Todo数
    quit_count = today_todos[today_todos['status'] == 3].shape[0]

    # [指标2] 平均专注时长
    # 逻辑：AVG(focus_time)，注意处理 NaN
    avg_focus_time = today_todos['focus_time'].mean()
    avg_focus_time = round(avg_focus_time, 2) if pd.notna(avg_focus_time) else 0.0

    # 4. 计算基于日志关联的指标
    # 逻辑：将今日计划与日志表关联
    # 注意：todo_log 中可能有多个日志对应一个 todo，这里假设取所有相关日志进行分析
    merged_df = pd.merge(
        today_todos[['id']],
        log_df,
        left_on='id',
        right_on='todo_id',
        how='left'
    )

    # [指标4] 平均满意度
    # 逻辑：AVG(score)，仅计算有日志记录的部分
    if not merged_df['score'].isna().all():
        avg_satisfaction = merged_df['score'].mean()
        avg_satisfaction = round(avg_satisfaction, 2)
    else:
        avg_satisfaction = 0.0

    # [指标3] 今日情绪画像
    # 逻辑：统计日志中 AI 预测的情绪词频，取出现频率最高的词
    # 剔除空值
    emotions = merged_df['emotion'].dropna()

    if not emotions.empty:
        # 使用 mode() 获取众数（出现次数最多的词）
        mode_result = emotions.mode()
        main_emotion = mode_result[0] if not mode_result.empty else "平静"
    else:
        main_emotion = "平静"  # 默认值

    # 5. 返回结果
    return {
        "今日待办完成率": round(completion_rate, 2),  # 保留两位小数，如 0.85
        "平均专注时长": avg_focus_time,
        "今日情绪画像": main_emotion,
        "平均满意度": avg_satisfaction,
        "中断/放弃数": quit_count
    }

# 周复盘


# ==========================================
# 使用示例 (模拟数据)
# ==========================================
if __name__ == "__main__":
    # 模拟 todo 表数据
    data_todo = {
        'id': [1, 2, 3, 4, 5],
        'deadline': [date(2026, 4, 19), date(2026, 4, 19), date(2026, 4, 19), date(2026, 4, 19), date(2026, 4, 18)],
        'status': [2, 2, 3, 0, 2],  # 2个完成, 1个放弃, 1个进行中, 1个是昨天的
        'focus_time': [45, 60, 10, 30, 50]
    }
    df_todo = pd.DataFrame(data_todo)
    print(df_todo)

    # 模拟 todo_log 表数据
    data_log = {
        'todo_id': [1, 2, 3],
        'score': [5, 4, 2],
        'emotion': ['兴奋', '兴奋', '疲惫'],
        'create_time': [datetime(2026, 4, 19, 9, 0), datetime(2026, 4, 19, 10, 0), datetime(2026, 4, 19, 11, 0)]
    }
    df_log = pd.DataFrame(data_log)

    # 调用函数
    target = date(2026, 4, 19)
    result = calculate_daily_metrics(df_todo, df_log, target)

    print(f"--- {target} 复盘报告 ---")
    for k, v in result.items():
        print(f"{k}: {v}")

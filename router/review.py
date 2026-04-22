"""
数据整体指标复盘接口
"""
import pandas as pd
from fastapi import HTTPException
from sqlalchemy import inspect, select
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr, upload
from crud.goal import goal
from crud.program import program
from crud.todo import todo, todo_log
from models.goal.goal import Goal, GoalCategory
from models.program import Program
from models.todo.todo_log import TodoLog
from models.users import User
from schemas.okr import *
from utils.auth import get_current_user
from utils.common import convert_to_year_okr_options, calculate_completion_rate, count_by_column, \
    convert_df_to_stack_chart_data, convert_counts_to_pie_data
from utils.response import Result
from utils.review.statistic_card import AccumulateStatisticCard

# 创建api-router实例
router = APIRouter(
    prefix='/api/review',
    tags=['review'],
)

indicator_calculator = AccumulateStatisticCard()


def goal_status_label(status: int) -> str:
    """
    目标状态标签
    :return:
    """
    if status == 0:
        return "待完成"
    elif status == 1:
        return "进行中"
    elif status == 2:
        return "已完成"
    elif status == 3:
        return "已放弃"


@router.get('/goal-review')
async def get_goal_review(
        year: int = Query(None, title='年', alias='endYear'),
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    统计具体年份的目标复盘指标
    :param year:
    :param db:
    :param current_user_id:
    :return:
    """
    # 1.-------------------------- 获取目标数据 --------------------------
    stmt = (select(Goal.id,
                   Goal.goal_category_id,
                   Goal.goal_status,
                   GoalCategory.category_name,
                   )
            .join(GoalCategory, Goal.goal_category_id == GoalCategory.id, isouter=True)
            .where(Goal.user_id == current_user_id))
    goal_result = await db.execute(stmt)
    goal_result = goal_result.mappings().all()

    data_list = []
    for row in goal_result:
        # 将 row 转为 dict
        item = dict(row)
        # 添加标签
        status_val = row['goal_status']
        item['goal_status_label'] = goal_status_label(status_val)
        data_list.append(item)

    if not data_list:
        return Result.success()
    goal_df = pd.DataFrame(data_list)

    # 1.1 -------------------------- 目标进度 --------------------------
    goal_completion = calculate_completion_rate(df=goal_df, column_name='goal_status', target_value=2)
    # 1.2 -------------------------- 目标分类饼图数据 --------------------------
    goal_cate_list = count_by_column(goal_df, 'category_name')
    # 1.3 -------------------------- 完成情况饼图数据 --------------------------
    goal_completion_list = count_by_column(goal_df, 'goal_status_label')
    # 1.4 -------------------------- 完成率曲线(待引入定时任务后查看) --------------------------
    # 1.5 -------------------------- 消费时间分布条形图数据 --------------------------
    stmt = (select(TodoLog.id,
                   TodoLog.program_id,
                   TodoLog.goal_id,
                   TodoLog.focus_time,
                   Program.program_name,
                   Goal.goal_name
                   )
            .join(Program, Program.id == TodoLog.program_id, isouter=True)
            .join(Goal, Goal.id == TodoLog.goal_id, isouter=True)
            .where(TodoLog.user_id == current_user_id))
    todo_log_result = await db.execute(stmt)
    todo_log_result = todo_log_result.mappings().all()
    todo_log_list = []
    for row in todo_log_result:
        # 将 row 转为 dict
        item = dict(row)
        todo_log_list.append(item)

    todo_log_df = pd.DataFrame(todo_log_list)
    consume_time_distribution_dict = convert_df_to_stack_chart_data(
        todo_log_df,
        'program_name',
        'goal_name',
        'focus_time')
    # 返回数据
    res_data = {
        'goalCompletion': float(goal_completion) * 100,
        'goalCateList': convert_counts_to_pie_data(goal_cate_list),
        'goalCompletionList': convert_counts_to_pie_data(goal_completion_list),
        'consumeTimeDistribution': consume_time_distribution_dict
    }
    return Result.success(data=res_data)

"""
数据整体指标复盘接口
"""
import pandas as pd
from fastapi import HTTPException
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.mysql_config import get_database
from crud import okr, upload
from crud.goal import goal
from crud.program import program
from crud.todo import todo, todo_log
from models.users import User
from schemas.okr import *
from utils.auth import get_current_user
from utils.common import convert_to_year_okr_options
from utils.response import Result
from utils.review.statistic_card import AccumulateStatisticCard

# 创建api-router实例
router = APIRouter(
    prefix='/api/dashboard',
    tags=['dashboard'],
)

indicator_calculator = AccumulateStatisticCard()


@router.get('/acc-statistic-card')
async def get_statistic_card(
        db: AsyncSession = Depends(get_database),
        current_user_id: int = Depends(get_current_user)
):
    """
    某用户累计数据指标卡数据接口。
    :param db:
    :param current_user_id:
    :return:
    """
    # 1. 获取目标数据
    goal_result = await goal.get_total_list(db, current_user_id)
    goal_list = [r.__dict__ for r in goal_result]
    goal_list = pd.DataFrame(goal_list)
    goal_indicator: dict = indicator_calculator.calculate_completion_stats(goal_list, status_col='goal_status')

    # 2. 获取项目数据
    program_result = await program.get_total_list(db, current_user_id)
    program_list = [r.__dict__ for r in program_result]
    program_list = pd.DataFrame(program_list)
    program_indicator: dict = indicator_calculator.calculate_completion_stats(program_list, status_col='program_status')

    # 3. 获取OKR数据
    okr_result = await okr.get_total_list(db, current_user_id)
    okr_list = [r.__dict__ for r in okr_result]
    okr_list = pd.DataFrame(okr_list)
    okr_indicator: dict = indicator_calculator.calculate_completion_stats(okr_list, completed_status_num=1)

    # 4. 获取todo数据
    todo_result = await todo.get_total_list(db, current_user_id)
    todo_list = [r.__dict__ for r in todo_result]
    todo_list = pd.DataFrame(todo_list)
    todo_indicator: dict = indicator_calculator.calculate_completion_stats(todo_list)

    # 5. 获取todo_log数据
    todo_log_result = await todo_log.get_total_list(db, current_user_id)
    todo_log_list = [r.__dict__ for r in todo_log_result]
    todo_log_list = pd.DataFrame(todo_log_list)

    # 6. 获取上传图像数据
    upload_image_result = await upload.get_total_list(db, current_user_id)
    upload_image_list = [r.__dict__ for r in upload_image_result]
    upload_image_list = pd.DataFrame(upload_image_list)

    # 7. 财务数据

    # 响应数据封装
    res_data = [
        {
            'title': '累计达成目标',
            'subtitle': f'完成率{goal_indicator["completion_rate"]}%',
            'value': goal_indicator['completed_count'],
            'targetValue': goal_indicator['total_count'],
            'unit': '项',
            'delta': '',
            'isPositive': None
        },
        {
            'title': '累计达成项目',
            'subtitle': f'完成率{goal_indicator["completion_rate"]}%',
            'value': program_indicator['completed_count'],
            'targetValue': program_indicator['total_count'],
            'unit': '项',
            'delta': '',
            'isPositive': None
        },
        {
            'title': '累计达成OKR',
            'subtitle': f'完成率{okr_indicator["completion_rate"]}%',
            'value': okr_indicator['completed_count'],
            'targetValue': okr_indicator['total_count'],
            'unit': '个',
            'delta': '',
            'isPositive': None
        },
        {
            'title': '累计完成TODO',
            'subtitle': f'完成率{todo_indicator["completion_rate"]}%',
            'value': todo_indicator['completed_count'],
            'targetValue': todo_indicator['total_count'],
            'unit': '项',
            'delta': '',
            'isPositive': None
        },
        {
            'title': '累计上传TODO日志',
            'subtitle': '',
            'value': int(todo_log_list['id'].count()),
            'targetValue': int(todo_log_list['id'].count()),
            'unit': '次',
            'delta': '',
            'isPositive': None
        },
        {
            'title': '累计记录的精彩瞬间',
            'subtitle': '',
            'value': int(upload_image_list['id'].count()),
            'targetValue': int(upload_image_list['id'].count()),
            'unit': '次',
            'delta': '',
            'isPositive': None
        }

    ]
    return Result.success(data=res_data)

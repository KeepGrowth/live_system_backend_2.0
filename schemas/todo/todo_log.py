from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


# 新增todo日志参数
class TodoLogAddRequest(BaseModel):
    user_id: int = Field(None, description="user id", alias="userId")
    todo_id: int = Field(None, description="todo id", alias="todoId")
    goal_id: Optional[int] = Field(None, description="goal id", alias="goalId")
    program_id: Optional[int] = Field(None, description="program id", alias="programId")
    okr_id: Optional[int] = Field(None, description="okr id", alias="okrId")
    title: str = Field(None, description="todo log title", alias="title")
    score: Optional[int] = Field(None, description="todo log score", alias="score")
    log_desc: Optional[str] = Field(None, description="todo log desc", alias="logDesc")
    emotion: Optional[str] = Field(None, description="日志情绪-AI预测生成", alias="emotion")
    attachment_path: Optional[str] = Field(None, description="todo log attachment path", alias="attachmentPath")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


class TodoLogUpdateRequest(TodoLogAddRequest):
    id: int = Field(None, description="todo log id", alias="id")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


class TodoLogQueryRequest(BaseModel):
    """
    下列参数为允许的条件参数。
    """
    user_id: int = Field(None, description="user id", alias="userId")
    todo_id: Optional[int] = Field(None, description="todo id", alias="todoId")
    start_date: Optional[date] = Field(None, description="开始时间", alias="startDate")
    end_date: Optional[date] = Field(None, description="结束时间", alias="endDate")
    goal_id: Optional[int] = Field(None, description="goal id", alias="goalId")
    program_id: Optional[int] = Field(None, description="program id", alias="programId")
    okr_id: Optional[int] = Field(None, description="okr id", alias="okrId")


class TodoLogItemResponse(TodoLogAddRequest):
    id: int = Field(None, description="todo log id", alias="id")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")


# 不分页查询列表返回数据模型
class TodoLogListResponse(BaseModel):
    total: int = Field(None, description="todo log 总数")
    todo_log_list: list[TodoLogItemResponse] = Field(default_factory=list, description="todo log 列表",
                                                     alias="todoLogList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

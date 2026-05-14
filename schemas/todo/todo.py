from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union
from datetime import date, datetime
from schemas.todo.todo_log import TodoLogItemResponse, TodoLogJoinItemResponse
from schemas.upload_images import UploadImagesResponse
from schemas.users import SafeUserResponse


# 新增todo数据校验
class TodoAddRequest(BaseModel):
    title: str = Field(None, description="todo名称", alias="title")
    todo_goal: Optional[str] = Field(None, description="todo目标描述", alias="todoGoal")
    finish_desc: Optional[str] = Field(None, description="完成描述", alias="finishDesc")
    quit_desc: Optional[str] = Field(None, description="放弃描述", alias="quitDesc")
    importance: Optional[int] = Field(None, description="todo重要程度：0紧急不重要，1紧急重要，2不紧急不重要，3不紧急重要",
                                      alias="importance")
    user_id: Optional[int] = Field(None, description="外键关联-用户id", alias="userId")
    status: Optional[int] = Field(None, description="todo状态：0待完成，1进行中，2已完成,3已放弃", alias="status")
    focus_time: Optional[int] = Field(None, description="todo专注时间(分钟)", alias="focusTime")
    deadline: Optional[Union[date, str]] = Field(None, description="todo截止时间", alias="deadline")
    goal_id: Optional[int] = Field(None, description="外键关联-目标id", alias="goalId")
    program_id: Optional[int] = Field(None, description="外键关联-项目id", alias="programId")
    okr_id: Optional[int] = Field(None, description="外键关联-OKR id", alias="okrId")
    attachment_path: Optional[str] = Field(None, description="todo附件路径", alias="attachmentPath")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 更新todo数据校验
class TodoUpdateRequest(TodoAddRequest):
    id: int = Field(None, description="todo id", alias="id")


# 条件查询数据校验
class TodoQueryRequest(BaseModel):
    """
    下列参数为允许的条件参数。
    """
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")
    start_date: Optional[date] = Field(None, description="开始时间", alias="startDate")
    end_date: Optional[date] = Field(None, description="结束时间", alias="endDate")
    status: Optional[int] = Field(None, description="todo状态：0待完成，1进行中，2已完成,3已放弃", alias="status")
    goal_id: Optional[int] = Field(None, description="外键关联-目标id", alias="goalId")
    program_id: Optional[int] = Field(None, description="外键关联-项目id", alias="programId")
    okr_id: Optional[int] = Field(None, description="外键关联-OKR id", alias="okrId")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 联表查询单个信息返回数据模型
class TodoJoinItemResponse(TodoAddRequest):
    id: int = Field(None, description="todo id", alias="id")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")
    kr_name: Optional[str] = Field(None, description="KR名称", alias="krName")
    program_name: Optional[str] = Field(None, description="项目名称", alias="programName")
    goal_name: Optional[str] = Field(None, description="目标名称", alias="goalName")
    # 关联信息
    todo_logs: Optional[list[TodoLogJoinItemResponse]] = Field(None, description="todo日志列表",
                                                               alias="todoLogList")
    user: Optional[SafeUserResponse] = Field(None, description="用户信息", alias="user")
    upload_images: Optional[list[UploadImagesResponse]] = Field(None, description="图片列表",
                                                                alias="imageList")


# 单个查询响应
class TodoItemResponse(TodoAddRequest):
    id: int = Field(None, description="todo id", alias="id")
    user: Optional[SafeUserResponse] = Field(None, description="用户信息", alias="user")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")
    image_urls: Optional[list[UploadImagesResponse]] = Field(default_factory=list, description="图片列表",
                                                             alias="imageList")


# 分页查询列表返回数据模型
class TodoListResponse(BaseModel):
    total: int = Field(None, description="todo总数")
    todo_list: list[TodoJoinItemResponse] = Field(default_factory=list, description="todo列表", alias="todoList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

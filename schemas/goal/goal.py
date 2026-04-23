from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict

from schemas.goal.goal_cate import GoalCategoryItemResponse
from schemas.program.program import ProgramItemResponse
from schemas.upload_images import UploadImagesResponse
from schemas.users import SafeUserResponse


# 新增数据校验模型
class GoalAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    goal_name: Optional[str] = Field(None, description="目标名称", alias="goalName")
    description: Optional[str] = Field(None, description="目标描述|预期达成结果", alias="description")
    goal_category_id: Optional[int] = Field(None, description="目标分类id", alias="goalCategoryId")
    goal_status: Optional[int] = Field(None, description="目标状态：0待完成，1进行中，2已完成,3已放弃",
                                       alias="goalStatus")
    satisfaction_score: Optional[int] = Field(None, description="目标计划满意度评分-满分5分",
                                              alias="satisfactionScore")
    start_date: Optional[date] = Field(None, description="目标计划开始时间", alias="startDate")
    finish_date: Optional[date] = Field(None, description="目标完成时间", alias="finishDate")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 更新数据校验模型
class GoalUpdateRequest(GoalAddRequest):
    id: int = Field(None, description="目标id", alias="id")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 条件查询参数
class GoalQueryParams(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    start_year: Optional[int] = Field(None, description="开始时间", alias="startYear")
    end_year: Optional[int] = Field(None, description="结束时间", alias="endYear")
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 单个目标信息返回数据模型
class GoalItemResponse(GoalAddRequest):
    id: int = Field(None, description="目标id", alias="id")
    user: Optional[SafeUserResponse] = Field(None, description="目标创建者信息", alias="user")
    goal_status_label: Optional[str] = Field(None, description="目标状态标签", alias="goalStatusLabel")
    goal_category: Optional[GoalCategoryItemResponse] = Field(None, description="目标分类名称", alias="goalCategory")
    upload_images: list[UploadImagesResponse] = Field(None, description="目标图片列表", alias="imageUrls")
    create_time_str: Optional[str] = Field(None, description="目标创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="目标更新时间", alias="updateTimeStr")


# 联表查询响应数据
class GoalJoinItemResponse(GoalAddRequest):
    id: int = Field(None, description="目标id", alias="id")
    user: Optional[SafeUserResponse] = Field(None, description="目标创建者信息", alias="user")
    goal_status_label: Optional[str] = Field(None, description="目标状态标签", alias="goalStatusLabel")
    goal_category: Optional[GoalCategoryItemResponse] = Field(None, description="目标分类名称", alias="goalCategory")
    programs: list[ProgramItemResponse] = Field(None, description="目标下的计划列表", alias="programList")
    upload_images: list[UploadImagesResponse] = Field(None, description="目标图片列表", alias="imageUrls")
    create_time_str: Optional[str] = Field(None, description="目标创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="目标更新时间", alias="updateTimeStr")


# 目标列表返回数据模型
class GoalListResponse(BaseModel):
    total: int = Field(None, description="目标总数", alias="total")
    goal_list: list[GoalJoinItemResponse] = Field(None, description="目标列表", alias="goalList")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

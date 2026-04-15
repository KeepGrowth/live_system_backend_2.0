from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# 新增数据校验模型
class GoalAddRequest(BaseModel):
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


# 单个目标信息返回数据模型
class GoalDetailResponse(GoalAddRequest):
    id: int = Field(None, description="目标id", alias="id")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 目标列表返回数据模型
class GoalListResponse(BaseModel):
    total: int = Field(None, description="目标总数", alias="total")
    goal_list: list[GoalDetailResponse] = Field(None, description="目标列表", alias="goalList")
    has_more: bool = Field(None, description="是否有更多", alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

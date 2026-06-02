from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# 新增数据校验模型
class GoalCategoryAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    category_name: Optional[str] = Field(None, description="目标分类名称", alias="categoryName")
    description: Optional[str] = Field(None, description="目标分类描述")

    model_config = ConfigDict(
        populate_by_name=True,  # 兼容字段名和alias
        from_attributes=True  # 支持从ORM对象加载
    )


# 更新数据校验模型
class GoalCategoryUpdateRequest(GoalCategoryAddRequest):
    id: int = Field(..., description="目标分类ID")  # 更新必须传ID，设为必填


# 条件查询参数
class GoalCategoryQueryParams(GoalCategoryAddRequest):
    user_id: Optional[int] = Field(None, description='用户ID', alias='userId')


# 单个目标分类信息返回数据模型
class GoalCategoryItemResponse(GoalCategoryAddRequest):
    id: int = Field(None, description="目标分类id", alias="id")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# 目标分类列表返回数据模型
class GoalCategoryListResponse(BaseModel):
    goal_category_list: List[GoalCategoryItemResponse] = Field(...,
                                                               description="目标分类列表",
                                                               alias="goalCategoryList")  # 驼峰alias

    model_config = ConfigDict(
        populate_by_name=True,  # 关键：兼容下划线字段名和驼峰alias
        from_attributes=True,
    )

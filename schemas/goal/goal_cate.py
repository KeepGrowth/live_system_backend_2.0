from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# 新增数据校验模型
class GoalCategoryAddRequest(BaseModel):
    category_name: Optional[str] = Field(None, description="目标分类名称", alias="categoryName")
    description: Optional[str] = Field(None, description="目标分类描述")

    model_config = ConfigDict(
        populate_by_name=True,  # 兼容字段名和alias
        from_attributes=True  # 支持从ORM对象加载
    )


# 更新数据校验模型（继承父类配置，无需重复写）
class GoalCategoryUpdateRequest(GoalCategoryAddRequest):
    id: int = Field(..., description="目标分类ID")  # 更新必须传ID，设为必填


# 单个目标分类信息返回数据模型
class GoalCategoryDetailResponse(GoalCategoryAddRequest):
    id: int = Field(None, description="目标分类id", alias="id")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")  # 前端用驼峰，alias改驼峰
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")  # 统一驼峰alias

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


# 目标分类列表返回数据模型（核心修复：解决ValidationError）
class GoalCategoryListResponse(BaseModel):
    total: int = Field(..., description="目标分类总数", alias="total")
    goal_category_list: List[GoalCategoryDetailResponse] = Field(...,
                                                                 description="目标分类列表",
                                                                 alias="goalCategoryList")  # 驼峰alias
    has_more: bool = Field(..., description="是否有更多", alias="hasMore")  # 驼峰alias

    model_config = ConfigDict(
        populate_by_name=True,  # 关键：兼容下划线字段名和驼峰alias
        from_attributes=True,
        exclude_none=True  # 排除None字段
    )

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from models.weight import Weight


# 体重基础数据模型
class WeightItem(BaseModel):
    id: int = Field(None, description="weightId",alias="id")
    weight: float = Field(None, description="体重", alias="weight")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 体重列表响应数据校验模型
class WeightListResponse(BaseModel):
    total: int = Field(None, description="总条数")
    has_more: bool = Field(None, description="是否有更多", alias="hasMore")
    weight_list: list[WeightItem] = Field(None, description="体重记录列表",alias="weightList")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 体重新增请求数据类型
class WeightAddRequest(BaseModel):
    weight: float = Field(None, description="体重", alias="weight")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 体重更新数据请求类型
class WeightUpdateRequest(BaseModel):
    id: int = Field(None, description="weightId")
    weight: float = Field(None, description="体重", alias="weight")

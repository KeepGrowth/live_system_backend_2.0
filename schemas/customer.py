from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from models.customer import Customer


# 新增客户[请求]数据校验模型
class CustomerAddRequest(BaseModel):
    customer_name: Optional[str] = Field(..., description="客户名称", alias="customerName")
    customer_desc: Optional[str] = Field(..., description="客户描述", alias="customerDesc")
    link_way: Optional[str] = Field(..., description="联系方式", alias="linkWay")
    degree: Optional[int] = Field(..., description="客户等级：0普通客户，1重要客户，2重要客户", alias="degree")
    img_url: Optional[str] = Field(None, description="客户图片|头像路径", alias="imgUrl")
    gender: Optional[int] = Field(..., description="客户性别：0未知，1男，2女", alias="gender")
    customer_field_id: Optional[int] = Field(..., description="客户行业id", alias="customerFieldId")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 客户基类
class CustomerBase(BaseModel):
    id: int = Field(..., description="客户id", alias="id")
    customer_name: str = Field(..., description="客户名称", alias="customerName")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 客户信息类
class CustomerInfoBase(CustomerBase):
    customer_desc: str = Field(..., description="客户描述", alias="customerDesc")
    link_way: str = Field(..., description="联系方式", alias="linkWay")
    degree: int = Field(..., description="客户等级：0普通客户，1重要客户，2重要客户", alias="degree")
    img_url: Optional[str] = Field(None, description="客户图片|头像路径", alias="imgUrl")
    gender: int = Field(..., description="客户性别：0未知，1男，2女", alias="gender")
    customer_field_id: int = Field(..., description="客户行业id", alias="customerFieldId")
    create_time: date = Field(..., description="创建时间", alias="createTime")
    update_time: date = Field(..., description="更新时间", alias="updateTime")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 客户信息响应数据校验模型
class CustomerItemResponse(CustomerInfoBase):
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 客户信息更新[请求]数据校验模型
class CustomerUpdateRequest(BaseModel):
    id: int = Field(..., description="客户id", alias="id")
    customer_name: Optional[str] = Field(..., description="客户名称", alias="customerName")
    customer_desc: Optional[str] = Field(..., description="客户描述", alias="customerDesc")
    link_way: Optional[str] = Field(..., description="联系方式", alias="linkWay")
    degree: Optional[int] = Field(..., description="客户等级：0普通客户，1重要客户，2重要客户", alias="degree")
    img_url: Optional[str] = Field(None, description="客户图片|头像路径", alias="imgUrl")
    gender: Optional[int] = Field(..., description="客户性别：0未知，1男，2女", alias="gender")
    customer_field_id: Optional[int] = Field(..., description="客户行业id", alias="customerFieldId")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 客户列表响应数据校验模型
class CustomerListResponse(BaseModel):
    total: int = Field(..., description="客户总数")
    customer_list: list[CustomerItemResponse] = Field(..., description="客户列表", alias="customerList")
    has_more: bool = Field(..., description="是否有更多", alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

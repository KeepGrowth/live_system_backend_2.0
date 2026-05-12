from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime

from schemas.upload_images import UploadImagesResponse


# 收入实体属性
class IncomeAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    first_cate_id: Optional[int] = Field(None, description="收入一级分类id", alias="firstCateId")
    second_cate_id: Optional[int] = Field(None, description="收入二级分类id", alias="secondCateId")
    amount: Optional[float] = Field(None, description="金额", alias="amount")
    income_date: Optional[date] = Field(None, description="收入时间", alias="incomeDate")
    note: Optional[str] = Field(None, description="备注", alias="note")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 收入查询参数
class IncomeQueryParams(IncomeAddRequest):
    id: Optional[int] = Field(None, description="收入id", alias="id")
    start_date: Optional[date] = Field(None, description="开始时间", alias="startDate")
    end_date: Optional[date] = Field(None, description="结束时间", alias="endDate")
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")
    keyword: Optional[str] = Field(None, description="关键字", alias="keyword")


# 收入更新参数
class IncomeUpdateRequest(IncomeAddRequest):
    id: int = Field(None, description="收入id", alias="id")


# 收入响应
class IncomeItemResponse(IncomeAddRequest):
    id: int = Field(None, description="收入id", alias="id")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# 收入列表响应
class IncomeListResponse(BaseModel):
    total: int = Field(None, description="收入总数")
    income_list: list[IncomeItemResponse] = Field(None, description="收入列表", alias="incomeList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 关联收入响应
class IncomeJoinItemResponse(IncomeItemResponse):
    first_cate_name: Optional[str] = Field(None, description="收入一级分类名称", alias="firstCateName")
    second_cate_name: Optional[str] = Field(None, description="收入二级分类名称", alias="secondCateName")


# 关联收入列表响应
class IncomeJoinListResponse(BaseModel):
    total: int = Field(None, description="收入总数")
    income_list: list[IncomeJoinItemResponse] = Field(None, description="收入列表", alias="incomeList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

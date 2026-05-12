from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


# 收入一级分类实体属性
class IncomeFirstCateAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 收入一级分类响应
class IncomeFirstCateItemResponse(IncomeFirstCateAddRequest):
    id: int = Field(None, description="收入一级分类id", alias="id")
    first_cate_name: str = Field(None, description="收入一级分类名称", alias="firstCateName")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# 收入一级分类列表响应
class IncomeFirstCateListResponse(BaseModel):
    total: int = Field(None, description="收入一级分类总数")
    income_first_cate_list: list[IncomeFirstCateItemResponse] = Field(None, description="收入一级分类列表",
                                                                      alias="incomeFirstCateList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

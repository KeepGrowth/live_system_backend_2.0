from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


# 收入二级分类实体属性
class IncomeSecondCateAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    second_cate_id: Optional[int] = Field(None, description="收入二级分类id", alias="firstCateId")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 收入二级分类响应
class IncomeSecondCateItemResponse(IncomeSecondCateAddRequest):
    id: int = Field(None, description="收入二级分类id", alias="id")
    second_cate_name: str = Field(None, description="收入二级分类名称", alias="secondCateName")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# 收入二级分类列表响应
class IncomeSecondCateListResponse(BaseModel):
    total: int = Field(None, description="收入二级分类总数")
    income_second_cate_list: list[IncomeSecondCateItemResponse] = Field(None, description="收入二级分类列表",
                                                                        alias="incomeSecondCateList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

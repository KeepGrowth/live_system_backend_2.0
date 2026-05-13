from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime

from schemas.upload_images import UploadImagesResponse


# 支出实体属性
class ExpenseAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    okr_id: Optional[int] = Field(None, description="OKR id", alias="okrId")
    program_id: Optional[int] = Field(None, description="项目id", alias="programId")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    first_cate_id: Optional[int] = Field(None, description="支出一级分类id", alias="firstCateId")
    second_cate_id: Optional[int] = Field(None, description="支出二级分类id", alias="secondCateId")
    amount: Optional[float] = Field(None, description="金额", alias="amount")
    image_list: Optional[list[dict]] = Field(None, description="图片列表", alias="imageList")
    expense_date: Optional[date] = Field(None, description="支出时间", alias="expenseDate")
    note: Optional[str] = Field(None, description="备注", alias="note")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 支出查询参数
class ExpenseQueryParams(ExpenseAddRequest):
    id: Optional[int] = Field(None, description="支出id", alias="id")
    start_date: Optional[date] = Field(None, description="开始时间", alias="startDate")
    end_date: Optional[date] = Field(None, description="结束时间", alias="endDate")
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")
    keyword: Optional[str] = Field(None, description="关键字", alias="keyword")


# 支出更新参数
class ExpenseUpdateRequest(ExpenseAddRequest):
    id: int = Field(None, description="支出id", alias="id")


# 支出响应
class ExpenseItemResponse(ExpenseAddRequest):
    id: int = Field(None, description="支出id", alias="id")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# 支出列表响应
class ExpenseListResponse(BaseModel):
    total: int = Field(None, description="支出总数")
    expense_list: list[ExpenseItemResponse] = Field(None, description="支出列表", alias="expenseList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 关联支出响应
class ExpenseJoinItemResponse(ExpenseItemResponse):
    first_cate_name: Optional[str] = Field(None, description="支出一级分类名称", alias="firstCateName")
    second_cate_name: Optional[str] = Field(None, description="支出二级分类名称", alias="secondCateName")


# 关联支出列表响应
class ExpenseJoinListResponse(BaseModel):
    total: int = Field(None, description="支出总数")
    expense_list: list[ExpenseJoinItemResponse] = Field(None, description="支出列表", alias="expenseList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

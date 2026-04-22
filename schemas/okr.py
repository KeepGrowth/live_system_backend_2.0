from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from schemas.todo.todo import TodoItemResponse
from schemas.upload_images import UploadImagesResponse
from schemas.users import SafeUserResponse


# 新增OKR[请求]数据校验模型
class OkrAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    program_id: Optional[int] = Field(None, description="项目id", alias="programId")
    status: Optional[int] = Field(None, description="状态：0待完成，1已完成，2已放弃", alias="status")
    kr_name: Optional[str] = Field(None, description="KR名称", alias="krName")
    kr_desc: Optional[str] = Field(None, description="KR描述", alias="krDesc")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 更新OKR[请求]数据校验模型
class OkrUpdateRequest(OkrAddRequest):
    id: Optional[int] = Field(None, description="OKR id", alias="id")


# 条件查询请求参数
class OkrQueryParams(OkrAddRequest):
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")


# 联表查询 单个信息响应数据校验模型
class OkrJoinItemResponse(OkrAddRequest):
    id: int = Field(None, description="OKR id", alias="id")
    todos: Optional[list[TodoItemResponse]] = Field(None, description="OKR关联的待办事项列表", alias="todoList")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")
    image_urls: Optional[list[UploadImagesResponse]] = Field(None, description="图片列表", alias="imageUrls")


# 单个信息响应数据校验模型
class OkrItemResponse(OkrAddRequest):
    id: int = Field(None, description="OKR id", alias="id")
    user: Optional[SafeUserResponse] = Field(None, description="用户名称", alias="user")
    image_urls: Optional[list[UploadImagesResponse]] = Field(None, description="图片列表", alias="imageUrls")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    update_time_str: Optional[str] = Field(None, description="更新时间", alias="updateTimeStr")


# OKR列表响应数据校验模型
class OkrListResponse(BaseModel):
    total: int = Field(None, description="OKR总数")
    okr_list: list[OkrItemResponse] = Field(None, description="OKR列表", alias="okrList")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

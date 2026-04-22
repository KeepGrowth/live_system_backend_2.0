from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from schemas.okr import OkrItemResponse, OkrJoinItemResponse
from schemas.program.program_log import ProgramLogItemResponse
from schemas.upload_images import UploadImagesResponse
from schemas.users import SafeUserResponse


# 新增项目[请求]数据校验模型
class ProgramAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    program_name: Optional[str] = Field(None, description="项目名称", alias="programName")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    program_desc: Optional[str] = Field(None, description="项目描述|预期达成结果", alias="programDesc")
    program_status: Optional[int] = Field(None, description="项目状态：0待完成，1进行中，2已完成,3已放弃",
                                          alias="programStatus")
    attachment_path: Optional[str] = Field(None, description="项目附件路径", alias="attachmentPath")
    satisfaction_score: int = Field(None, description="项目满意度评分-满分5分",
                                    alias="satisfactionScore")
    estimate_finish_time: Optional[date] = Field(None, description="项目预估完成时间",
                                                 alias="estimateFinishTime")
    estimate_start_time: Optional[date] = Field(None, description="项目预估开始时间",
                                                alias="estimateStartTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 更新项目[请求]数据校验模型
class ProgramUpdateRequest(ProgramAddRequest):
    id: Optional[int] = Field(None, description="项目id", alias="programId")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 条件查询请求参数
class ProgramQueryParams(ProgramUpdateRequest):
    page: Optional[int] = Field(1, description="页码", alias="page")
    page_size: Optional[int] = Field(1000, description="每页数量", alias="pageSize")


# 单个项目信息响应数据校验模型
class ProgramJoinItemResponse(ProgramAddRequest):
    id: Optional[int] = Field(None, description="项目id", alias="id")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")
    # 关联信息
    program_log: Optional[ProgramLogItemResponse] = Field(None, description="项目日志", alias="programLog")
    # 一对多信息
    okrs: Optional[list[OkrItemResponse]] = Field(None, description="项目OKR列表", alias="okrList")
    upload_images: Optional[list[UploadImagesResponse]] = Field(None, description="项目图片列表", alias="imageUrls")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


class ProgramItemResponse(ProgramAddRequest):
    id: Optional[int] = Field(None, description="项目id", alias="id")
    user: Optional[SafeUserResponse] = Field(None, description="项目创建者信息", alias="user")
    program_log: Optional[ProgramLogItemResponse] = Field(None, description="项目日志", alias="programLog")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")
    upload_images: Optional[list[UploadImagesResponse]] = Field(None, description="项目图片列表", alias="imageUrls")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 项目列表响应数据校验模型
class ProgramListResponse(BaseModel):
    total: int = Field(..., description="项目总数")
    program_list: list[ProgramItemResponse] = Field(None, description="项目列表", alias="programList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

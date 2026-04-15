from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from models.program import Program


# 新增项目[请求]数据校验模型
class ProgramAddRequest(BaseModel):
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    program_name: str = Field(None, description="项目名称", alias="programName")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    program_desc: str = Field(None, description="项目描述|预期达成结果", alias="programDesc")
    program_status: int = Field(None, description="项目状态：0待完成，1进行中，2已完成,3已放弃", alias="programStatus")
    attachment_path: Optional[str] = Field(None, description="项目附件路径", alias="attachmentPath")
    satisfaction_score: int = Field(None, description="项目满意度评分-满分5分",
                                    alias="SatisfactionScore")
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
    id: int = Field(..., description="项目id", alias="programId")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 条件查询请求参数
class ProgramQueryParams(ProgramUpdateRequest):
    page: Optional[int] = Field(None, description="页码", alias="page")
    page_size: Optional[int] = Field(None, description="每页数量", alias="pageSize")


# 单个项目信息响应数据校验模型
class ProgramItemResponse(ProgramAddRequest):
    id: int = Field(None, description="项目id", alias="id")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 项目列表响应数据校验模型
class ProgramListResponse(BaseModel):
    total: int = Field(..., description="项目总数")
    program_list: list[ProgramItemResponse] = Field(None, description="项目列表", alias="programList")
    has_more: bool = Field(..., description="是否有更多", alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

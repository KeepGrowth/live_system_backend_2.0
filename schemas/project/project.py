from typing import Optional, List  # 替换list为List，兼容更优
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# 新增单子[请求]数据校验模型
class ProjectAddRequest(BaseModel):
    # 核心字段设为必填（业务上单子名称/金额不能为空）
    project_name: str = Field(None, description="单子名称", alias="projectName")
    amount: float = Field(None, description="单子金额", alias="amount")

    # 非核心字段设为可选
    project_stack: Optional[str] = Field(None, description="单子技术栈描述", alias="projectStack")
    project_desc: Optional[str] = Field(None, description="单子描述", alias="projectDesc")
    status: Optional[int] = Field(None, description="单子状态", alias="status")
    start_date: Optional[date] = Field(None, description="单子开始时间", alias="startDate")
    end_date: Optional[date] = Field(None, description="单子结束时间", alias="endDate")
    channel_id: Optional[int] = Field(None, description="单子来源渠道id", alias="channelId")
    customer_id: Optional[int] = Field(None, description="单子客户id", alias="customerId")
    attachment_path: Optional[str] = Field(None, description="单子附件路径", alias="attachmentPath")
    cover_path: Optional[str] = Field(None, description="单子封面路径", alias="coverPath")

    model_config = ConfigDict(
        populate_by_name=True,  # 兼容下划线字段名和驼峰alias
        from_attributes=True,  # 支持ORM对象加载
        exclude_none=True  # 自动排除None字段，返回数据更简洁
    )


# 更新单子[请求]数据校验模型
class ProjectUpdateRequest(ProjectAddRequest):
    id: int = Field(..., description="单子id", alias="id")  # 更新必须传ID，设为必填
    # 继承父类的model_config，无需重复定义


# 单子单个详情响应数据
class ProjectDetailResponse(ProjectAddRequest):
    id: int = Field(None, description="单子id", alias="id")  # 响应时可为None，改为非必填
    create_time: datetime = Field(None, description="单子创建时间", alias="createTime")
    update_time: datetime = Field(None, description="单子更新时间", alias="updateTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,

    )


# 分页查询单子列表响应数据
class ProjectListResponse(BaseModel):
    total: int = Field(None, description="单子总数", alias="total")
    # 替换list[]为List[]，Pydantic更推荐的写法
    project_list: List[ProjectDetailResponse] = Field(None, description="单子列表", alias="projectList")
    has_more: bool = Field(None, description="是否有更多", alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

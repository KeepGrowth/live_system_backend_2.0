from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict


# 单子来源渠道单个详情响应数据

class ProjectChannelAddRequest(BaseModel):
    channel_name: str = Field(None, description="单子内容", alias="channelName")


class ProjectChannelDetailResponse(BaseModel):
    id: int = Field(None, description="单子来源渠道id", alias="id")
    channel_name: str = Field(None, description="单子来源渠道名称", alias="channel_name")
    create_time: datetime = Field(None, description="单子来源渠道创建时间", alias="create_time")
    update_time: datetime = Field(None, description="单子来源渠道更新时间", alias="update_time")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True,  # 允许从ORM对象属性中取
    )


# 单子来源渠道列表响应数据
class ProjectChannelListResponse(BaseModel):
    total: int = Field(None, description="总条数")
    has_more: bool = Field(None, description="是否有更多", alias="hasMore")
    channel_list: List[ProjectChannelDetailResponse] = Field(None, description="单子来源渠道列表", alias="channelList")
    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True,  # 允许

    )

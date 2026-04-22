from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from schemas.upload_images import UploadImagesResponse
from schemas.users import SafeUserResponse


# 单个项目日志响应模型
class ProgramLogItemResponse(BaseModel):
    id: Optional[int] = Field(None, description="项目日志id", alias="id")
    program_id: Optional[int] = Field(None, description="项目id", alias="programId")
    description: Optional[str] = Field(None, description="项目日志描述", alias="description")
    emotion: Optional[str] = Field(None, description="项目日志心情", alias="emotion")
    image_urls: Optional[list[UploadImagesResponse]] = Field(None, description="项目图片列表", alias="imageUrls")
    create_time: datetime = Field(None, description="创建时间", alias="createTime")
    update_time: datetime = Field(None, description="更新时间", alias="updateTime")
    user: Optional[SafeUserResponse] = Field(None, description="项目创建者信息", alias="user")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

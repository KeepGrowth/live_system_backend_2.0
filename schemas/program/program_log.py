from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime

from models.goal.goal import Goal
from models.okr import Okr
from models.program import Program, ProgramLog
from models.todo.todo import Todo
from models.todo.todo_log import TodoLog
from models.upload_images import UploadImages
from models.users import User
from schemas.goal.goal import GoalDetailResponse
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

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

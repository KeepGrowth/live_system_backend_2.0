from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from schemas.users import SafeUserResponse


# 单个图片响应数据模型
class UploadImagesResponse(BaseModel):
    id: Optional[int] = Field(None, description="图片id", alias="id")
    user_id: Optional[int] = Field(None, description="用户id", alias="userId")
    todo_log_id: Optional[int] = Field(None, description="待办事项日志id", alias="todoLogId")
    todo_id: Optional[int] = Field(None, description="待办事项id", alias="todoId")
    program_id: Optional[int] = Field(None, description="项目id", alias="programId")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    image_url: Optional[str] = Field(None, description="图片url", alias="imageUrl")
    create_time: Optional[datetime] = Field(None, description="创建时间", alias="createTime")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")

    user: Optional[SafeUserResponse] = Field(None, description="用户", alias="user")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )

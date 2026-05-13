from fastapi import Form
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
    okr_id: Optional[int] = Field(None, description="OKR id", alias="okrId")
    program_id: Optional[int] = Field(None, description="项目id", alias="programId")
    goal_id: Optional[int] = Field(None, description="目标id", alias="goalId")
    image_url: Optional[str] = Field(None, description="图片url", alias="imageUrl")
    create_time: Optional[datetime] = Field(None, description="创建时间", alias="createTime")
    create_time_str: Optional[str] = Field(None, description="创建时间", alias="createTimeStr")
    user: Optional[SafeUserResponse] = Field(None, description="用户信息", alias="user")

    model_config = ConfigDict(
        populate_by_name=True,  # alias 、字段名兼容
        from_attributes=True  # 允许从ORM对象属性中取值
    )


# 单个数据上传
from typing import Optional, Dict, Any
from fastapi import Form


class ImageUploadParams:
    def __init__(
            self,
            program_id: Optional[int] = Form(None, alias="programId"),
            goal_id: Optional[int] = Form(None, alias="goalId"),
            okr_id: Optional[int] = Form(None, alias="okrId"),
            todo_id: Optional[int] = Form(None, alias="todoId"),
            todo_log_id: Optional[int] = Form(None, alias="todoLogId"),
            expense_id: Optional[int] = Form(None, alias="expenseId"),
            income_id: Optional[int] = Form(None, alias="incomeId"),
    ):
        self.program_id = program_id
        self.goal_id = goal_id
        self.todo_id = todo_id
        self.okr_id = okr_id
        self.todo_log_id = todo_log_id
        self.image_url = None
        self.user_id = None
        self.expense_id = expense_id,
        self.income_id = income_id

    def to_non_empty_dict(self) -> Dict[str, Any]:
        """
        提取所有非 None 的字段为字典。
        键名使用 Python 属性名（例如 'program_id'）。
        """
        # vars(self) 等同于 self.__dict__，获取实例所有属性
        return {k: v for k, v in vars(self).items() if v is not None}

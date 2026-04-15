import json
from dataclasses import dataclass, asdict
from typing import Generic, TypeVar, Optional, Any

from sqlalchemy import JSON

# 定义泛型类型变量 T
T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    """
    统一返回结果
    RestFul 风格通用响应类
    """
    code: int
    msg: str
    data: Optional[T] = None

    def to_json(self) -> str:
        """
        将对象转换为 JSON 字符串
        """
        # asdict 将 dataclass 实例转换为字典
        return json.dumps(asdict(self), ensure_ascii=False)

    # ==================== 成功返回 ====================

    @staticmethod
    def success(data: Optional[T] = None, msg: str = "操作成功"):
        return Result(code=200, msg=msg, data=data)

    # ==================== 失败返回 ====================

    @staticmethod
    def error(msg: str = "操作失败", code: int = 500):
        return Result(code=code, msg=msg, data=None)

from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, UniqueConstraint, Float, JSON
from typing import Optional, List

from sqlalchemy.orm import relationship

from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# 系统日志基类
class SystemLogBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")


# 系统日志类
class SystemLog(SystemLogBase):
    __tablename__ = "system_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键")
    log_type: Mapped[str] = mapped_column(String(255), nullable=False, comment="日志类型")  # 高危|普通|风险
    method: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求方法")
    path: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求路径")
    client_ip: Mapped[str] = mapped_column(String(255), nullable=False, comment="客户端IP")
    status_code: Mapped[int] = mapped_column(Integer, nullable=False, comment="状态码")
    consume_time: Mapped[float] = mapped_column(Float, nullable=False, comment="耗时(ms)")
    # 请求参数->用JSON存储
    request_params: Mapped[str] = mapped_column(Text, nullable=True, comment="请求参数")

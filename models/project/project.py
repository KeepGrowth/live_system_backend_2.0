from sqlalchemy import func, Date, DateTime, String, Integer, ForeignKey, Text, Index, Double
from typing import Optional
from config.mysql_config import Base, mapped_column, Mapped
from datetime import date, datetime


# IT兼职项目基类
class ProjectBase(Base):
    __abstract__ = True
    create_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment="更新时间")


# IT兼职项目来源渠道分类
class ProjectChannel(ProjectBase):
    __tablename__ = "project_channel"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目来源渠道id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    channel_name: Mapped[Optional[str]] = mapped_column(String(50), unique=True, comment="项目来源渠道名称")


# IT兼职项目类
class Project(ProjectBase):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="项目id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="外键关联-用户id")
    project_name: Mapped[Optional[str]] = mapped_column(String(50), unique=False, comment="IT项目名称")
    # 技术栈描述
    project_stack: Mapped[str] = mapped_column(String(500), nullable=True, default="待完善", comment="技术栈描述")
    project_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="待完善", comment="项目描述")
    status: Mapped[int] = mapped_column(Integer, nullable=True, default=0,
                                        comment="项目状态：0待完成，1进行中，2已完成,3已放弃")
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="项目开始时间")
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="项目结束|截止时间")
    amount: Mapped[float] = mapped_column(Double, nullable=True, default=0, comment="项目金额|预期收入")
    channel_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('project_channel.id'), nullable=True,
                                                      comment="外键关联-来源渠道id")
    # 项目封面
    cover_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="项目封面路径")
    customer_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('customer.id'), nullable=True,
                                                       comment="外键关联-客户id")
    attachment_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="项目附件路径")

from sqlalchemy import func, ForeignKey

from config.mysql_config import Base, mapped_column, Mapped
from datetime import datetime


# 体重映射类基类
class WeightBase(Base):
    __abstract__ = True

    create_time: Mapped[datetime] = mapped_column(default=func.now(), comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(default=func.now(), comment="更新时间")


# 体重类
class Weight(WeightBase):
    __tablename__ = "weight"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="id")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, comment="用户id")
    weight: Mapped[float] = mapped_column(comment="体重", nullable=False, )

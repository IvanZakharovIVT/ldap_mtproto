from sqlalchemy import TIMESTAMP, Column, func

from app.core.database import Base


class BaseDBModel(Base):
    __abstract__ = True

    modified_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

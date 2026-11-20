from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    priority: Mapped[int]
    status: Mapped[str] = mapped_column(
        default="pending",
        server_default="pending"
    )
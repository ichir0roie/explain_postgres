# https://docs.sqlalchemy.org/en/20/orm/quickstart.html

# 流石にこんなインポートは良くないよね
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime, timedelta

engine = create_engine(
    "postgresql://user:password@localhost:54321/db", echo=True
)


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False, server_default=func.now()
    )

    pass


class Sample(Base):
    __tablename__ = "sample"

    str_a: Mapped[str]

    __table_args__ = {
        "comment": "sample table",
    }

# class User(Base):
#     __tablename__ = "user_account"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(
#         back_populates="user", cascade="all, delete-orphan"
#     )

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")

#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

if __name__ == "__main__":

    meta = Base.metadata
    meta.create_all(engine)

    with Session(engine) as session:
        sample = Sample()
        sample.str_a = "sample"
        session.add(sample)
        session.commit()

        res = session.scalars(select(Sample)).all()
        for r in res:
            print(r.__dict__)

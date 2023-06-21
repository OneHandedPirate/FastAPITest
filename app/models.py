from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey

from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,
                     ForeignKey("user.id", ondelete="CASCADE"),
                     nullable=False)
    salary = Column(DECIMAL(10, 2), nullable=False)
    promotion_date = Column(TIMESTAMP(timezone=True), nullable=False)

from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    location = Column(Text())
    market = Column(Text())
    website = Column(Text())
    employees = Column(Text())
    stage = Column(Text())
    total_raised = Column(Text())
    emails = relationship("Email", backref="company")


class Email(Base):
    __tablename__ = 'email'

    id = Column(Integer(), primary_key=True)
    name = Column(Text())
    company_id = Column(Integer, ForeignKey('company.id'))

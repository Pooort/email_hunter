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
    company_id = Column(Integer, ForeignKey('company.id'))
    value = Column(Text())
    first_name = Column(Text())
    last_name = Column(Text())
    position = Column(Text())
    seniority = Column(Text())
    department = Column(Text())
    linkedin = Column(Text())
    twitter = Column(Text())
    phone_number = Column(Text())
    type = Column(Text())

from datetime import datetime
from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Appointment(Base):

    """An appointment on the calendar."""
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now,
                      onupdate=datetime.now)
    title = Column(String(255))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(255))
    description = Column(Text)

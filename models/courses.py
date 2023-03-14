from sqlalchemy import Column, Integer, String, Boolean

from config.database import Base

class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    lines_of_work = Column(String)
    specific_objetives = Column(String)
    type_of_course = Column(String)
    status = Column(Boolean, default=True)
    
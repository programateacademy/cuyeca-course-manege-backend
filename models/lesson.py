from sqlalchemy import Column, Integer, String
from config.database import Base
from pydantic import UploadFile, File
class Lesson (Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    resource = Column(UploadFile[String])
    




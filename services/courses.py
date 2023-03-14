from operator import and_
from models.courses import Courses as CoursesModel
from schemas.courses import Courses

class CoursesService():
    def __init__(self,db) -> None:
        self.db = db

    def get_courses(self):
        result = self.db.query(CoursesModel).all()
        return result
    
    def get_courses_by_id(self, id:int):
        result = self.db.query(CoursesModel).filter (and_(CoursesModel.id == id , CoursesModel.status == True)).first()
        return result
    
    def get_courses_by_name(self, name:str):
        result = self.db.query(CoursesModel).filter(CoursesModel.name == name).first()
        return result
    
    def create_courses(self, courses:Courses):
        new_courses = CoursesModel(
            id= courses.id,
            name= courses.name,
            description= courses.description,
            lines_of_work= courses.lines_of_work,
            specific_objetives= courses.specific_objetives,
            type_of_course= courses.type_of_course
        )
        self.db.add(new_courses)
        self.db.commit()
        return
    
    def update_courses(self,id:int, data:Courses):
        courses = self.db.query(CoursesModel).filter(CoursesModel.id == id).first()
        courses.name = data.name
        courses.description = data.description
        courses.lines_of_work = data.lines_of_work
        courses.specific_objetives = data.specific_objetives
        courses.type_of_course = data.type_of_course
        self.db.commit()
        return
    
    def update_courses_by_name(self,name:str, data:Courses):
        courses = self.db.query(CoursesModel).filter(CoursesModel.name == name).first()
        courses.description = data.description
        courses.lines_of_work = data.lines_of_work
        courses.specific_objetives = data.specific_objetives
        courses.type_of_course = data.type_of_course
        self.db.commit()
        return
    
    def update_status_course(self, id:int):
        courses = self.db.query(CoursesModel).filter(CoursesModel.id == id).first()
        courses.status = False
        self.db.commit()
        return
    
    def delete_courses(self, id:int):
        self.db.query(CoursesModel).filter(CoursesModel.id == id).delete()
        self.db.commit()
        return
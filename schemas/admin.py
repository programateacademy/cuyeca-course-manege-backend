import datetime as _dt
import pydantic as _pydantic

class _SuperadminBase(_pydantic.BaseModel):
    email:str
    

class SuperadminCreate(_SuperadminBase):
    password:str
    username:str
    
    class Config:
        orm_mode = True
        


class Superadmin(_SuperadminBase):
    id: int
    
    class Config:
        orm_mode = True

class _AdminBase(_pydantic.BaseModel):
    username:str
    password:str
    
class AdminCreate(_AdminBase):
    pass

class Admin(_AdminBase):
    id: int
    owner_id:int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime
    
    class Config:
        orm_mode = True

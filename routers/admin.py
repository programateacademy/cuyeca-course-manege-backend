from fastapi import APIRouter
from typing import List
from schemas.admin import Admin
from fastapi import FastAPI
import fastapi as _fastapi
from config.database import Session, engine, Base
from middlewares.error_handler import Errorhandler

from routers.courses import courses_router
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services.admin as _serviceadmin
import schemas.admin as _schemaadmin

admin_router = APIRouter()

@admin_router.post("/api/superadmin", tags=['superadmin'])
async def create_superadmin(superadmin:_schemaadmin.SuperadminCreate,db: _orm.Session = _fastapi.Depends(_serviceadmin.get_db)):
    db_superadmin = await _serviceadmin.get_superadmin_by_email(superadmin.email,db)
    if db_superadmin:
        raise _fastapi.HTTPException(status_code=400, detail= "Email already exists in superadmin")
    superadmin= await _serviceadmin.create_superadmin(superadmin,db)
    
    return await _serviceadmin.create_token(superadmin)

@admin_router.post("/api/token", tags=['superadmin'])
async def generate_token(form_data:_security.OAuth2PasswordRequestForm = _fastapi.Depends(),db:_orm.Session = _fastapi.Depends(_serviceadmin.get_db)):
    superadmin = await _serviceadmin.authenticate_superadmin(form_data.username, form_data.password,db)
    
    if not superadmin:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    
    return await _serviceadmin.create_token(superadmin)

@admin_router.get("/api/superadmin/me", tags=['superadmin'], response_model=_schemaadmin.Superadmin)
async def get_superadmin(superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin) ):
    return superadmin  

# ROUTES TO ADMINS

@admin_router.post("/api/admins",  tags=['admins'],response_model=_schemaadmin.Admin)
async def create_admin(admin: _schemaadmin.AdminCreate, superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin),db:_orm.Session = _fastapi.Depends(_serviceadmin.get_db)):
    return await _serviceadmin.create_admin(superadmin=superadmin,db=db, admin=admin)


@admin_router.get("/api/admins", tags=['admins'],response_model=List[_schemaadmin.Admin])
async def get_admins(
    superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin),
    db:_orm.Session = _fastapi.Depends(_serviceadmin.get_db),
):
    return await _serviceadmin.get_admins(superadmin=superadmin,db=db)

@admin_router.get("/api/admins/{admin_id}",tags=['admins'], status_code=200)
async def get_admin(
    admin_id:int,
    superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin),
    db:_orm.Session =_fastapi.Depends(_serviceadmin.get_db),
    ):
    return await _serviceadmin.get_admin(admin_id,superadmin,db)


@admin_router.delete("/api/admins/{admin_id}",tags=['admins'], status_code=204)
async def delete_admin( 
    admin_id:int,
    superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin),
    db:_orm.Session =_fastapi.Depends(_serviceadmin.get_db)):
    
    await _serviceadmin.delete_admin(admin_id,superadmin,db)
    return{"message", "administrador eliminado satisfactoriamente"}

@admin_router.put("/api/admins/{admin_id}",tags=['admins'], status_code=200)
async def update_admin( 
    admin_id:int,
    admin: _schemaadmin.AdminCreate,
    superadmin: _schemaadmin.Superadmin = _fastapi.Depends(_serviceadmin.get_current_superadmin),
    db:_orm.Session =_fastapi.Depends(_serviceadmin.get_db)):
    await _serviceadmin.update_admin(admin_id,admin,superadmin,db)
    return{"message", "administrador actualizado satisfactoriamente"}



# this is a endpoint to prove react with fastapi
@admin_router.get("/api", tags=['admins'])
async def root():
    return{"message":"Creación administradores"}


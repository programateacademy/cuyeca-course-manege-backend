from fastapi import FastAPI
import fastapi as _fastapi
from config.database import Session, engine, Base
from middlewares.error_handler import Errorhandler

from routers.courses import courses_router
from routers.admin import admin_router
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services.admin as _serviceadmin
import schemas.admin as _schemaadmin



app = FastAPI()
app.title = "App with fastAPI and react"

app.add_middleware(Errorhandler)

app.include_router(courses_router)
app.include_router(admin_router)



Base.metadata.create_all(bind=engine)




import fastapi as _fastapi
import fastapi.security as _security
import config.database as _database
import models.admin as _modeladmin
import schemas.admin as _schemaadmin
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt as _jwt
import datetime as _dt


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"

def create_database():
    return _database.Base.create_all(bind=_database.engine)

def get_db():
    db = _database.Session()
    try:
        yield db 
    finally:
        db.close()

async def get_superadmin_by_email(email:str, db:_orm.Session):
    return db.query(_modeladmin.Superadmin).filter(_modeladmin.Superadmin.email == email).first()

# function with hash to create password
async def create_superadmin(superadmin:_schemaadmin.SuperadminCreate, db:_orm.Session):
    superadmin_obj = _modeladmin.Superadmin(email=superadmin.email,username=superadmin.username,password=_hash.bcrypt.hash(superadmin.password))
    db.add(superadmin_obj)
    db.commit()
    db.refresh(superadmin_obj)
    return superadmin_obj

# function to authenticate superadmin

async def authenticate_superadmin(email:str,password:str,db:_orm.Session):
    superadmin = await get_superadmin_by_email(db=db,email=email)
    
    if not superadmin:
        return False
    
    if not superadmin.verify_password(password):
        return False
    
    return superadmin


async def create_token(superadmin:_modeladmin.Superadmin):
    superadmin_obj= _schemaadmin.Superadmin.from_orm(superadmin)
    
    token = _jwt.encode(superadmin_obj.dict(), JWT_SECRET)
    
    return dict(access_token=token, token_type="bearer")

async def get_current_superadmin(db:_orm.Session = _fastapi.Depends(get_db), token:str = _fastapi.Depends(oauth2schema)):
    try: 
        payload = _jwt.decode(token,JWT_SECRET, algorithms=["HS256"])
        superadmin = db.query(_modeladmin.Superadmin).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")
    
    return _schemaadmin.Superadmin.from_orm(superadmin)

# services to admin

async def create_admin(superadmin:_schemaadmin.Superadmin, db:_orm.Session, admin:_schemaadmin.AdminCreate):
    admin = _modeladmin.Admin(**admin.dict(), owner_id =superadmin.id)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return _schemaadmin.Admin.from_orm(admin)

async def get_admins(superadmin:_schemaadmin.Superadmin, db:_orm.Session):
    admins = db.query(_modeladmin.Admin).filter_by(owner_id=superadmin.id)
    return list(map(_schemaadmin.Admin.from_orm, admins))

async def _admin_selector(admin_id:int,superadmin:_schemaadmin.Superadmin, db:_orm.Session):
    admin = ( db.query(_modeladmin.Admin).filter_by(owner_id = superadmin.id).filter(_modeladmin.Admin.id == admin_id).first())
    if admin is None:
        raise _fastapi.HTTPException(status_code=404, detail="El administrador no existe")
    return admin

async def get_admin(admin_id:int,superadmin:_schemaadmin.Superadmin, db:_orm.Session):
    admin = await _admin_selector(admin_id=admin_id, superadmin=superadmin, db=db)
    
    return _schemaadmin.Admin.from_orm(admin)

async def delete_admin(admin_id:int,superadmin:_schemaadmin.Superadmin, db:_orm.Session):
    admin = await _admin_selector(admin_id,superadmin,db)
    
    db.delete(admin)
    db.commit()
    
    
async def update_admin(admin_id:int,admin:_schemaadmin.AdminCreate,superadmin:_schemaadmin.Superadmin, db:_orm.Session):
    admin_db = await _admin_selector(admin_id, superadmin, db)
    
    admin_db.username = admin.username
    admin_db.password = admin.password
    admin_db.date_last_updated = _dt.datetime.utcnow()
    
    db.commit()
    db.refresh(admin_db)
    
    return _schemaadmin.Admin.from_orm(admin_db)


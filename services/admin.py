import fastapi as _fastapi
import fastapi.security as _security
import config.database as _database
import models.admin as _modeladmin
import schemas.admin as _schemaadmin
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt as _jwt


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
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import config.database as _database
import datetime as _dt



class Superadmin(_database.Base):
    __tablename__='superadmin'
    id = _sql.Column(_sql.Integer, primary_key=True)
    username = _sql.Column(_sql.String(15),nullable = False) 
    password = _sql.Column(_sql.String(10),nullable = False)
    email = _sql.Column(_sql.String(20),nullable = False)
    admins = _orm.relationship("Admin", back_populates="owner") 

    def verify_password(self, password:str):
        return _hash.bcrypt.verify(password, self.password)

class Admin (_database.Base):
    __tablename__='admins'
    id = _sql.Column(_sql.Integer, primary_key=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("superadmin.id"))
    username = _sql.Column(_sql.String(15),nullable = False) 
    password = _sql.Column(_sql.String(10),nullable = False)
    date_created = _sql.Column(_sql.DateTime, default = _dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default = _dt.datetime.utcnow)
    owner = _orm.relationship("Superadmin", back_populates = "admins")

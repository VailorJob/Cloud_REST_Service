from cloud_server import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)
    access_key_id = db.Column(db.String(500), nullable=True)
    secret_access_key = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<users_id {self.id}; users_login {self.login}>"

db.create_all()


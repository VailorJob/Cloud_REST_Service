from cloud_server import db, app


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(500), nullable=True)
    access_key_id = db.Column(db.String(500), nullable=True)
    secret_access_key = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<users_id {self.id}; users_login {self.login}>"

    def __call__(self, _type="dict"):
        if _type == "dict":
            return {
                "id": self.id,
                "login": self.login,
                "password": self.password,
                "access_key_id": self.access_key_id,
                "secret_access_key": self.secret_access_key
            }
        elif _type == "list":
            return [self.id, self.login, self.password, self.access_key_id, self.secret_access_key]


with app.app_context():
    db.create_all()

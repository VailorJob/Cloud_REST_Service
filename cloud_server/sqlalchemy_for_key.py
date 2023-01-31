from sqlalchemy import create_engine, Table, Column, MetaData, Integer, String, exc
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

aws_access_key_id = f.encrypt("AKIA4P2WYEPXYKQ6RE54".encode())
aws_secret_access_key = f.encrypt("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".encode())

# print([f.decrypt(aws_access_key_id).decode("UTF-8"), f.decrypt(aws_secret_access_key).decode("UTF-8")])

class SQLAlchemyForKeys:
    _engine = create_engine('sqlite:///keyforaws.db', echo = True)
    _metadata = MetaData()
    keys = Table('secret_keys', _metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('access_key_id', String, nullable=False),
            Column('secret_access_key', String, nullable=False),
            Column('key_secret', String, nullable=False)
        )

    try:
        keys.create(_engine)
    except exc.OperationalError:
        pass

    @classmethod
    def insert_keys(cls, access_key_id, secret_access_key, key_secret):
        with cls._engine.connect() as conn:
            conn.execute(cls.keys.insert().values(access_key_id=access_key_id, secret_access_key=secret_access_key, key_secret=key_secret))
            conn.commit()

    @classmethod
    def get_keys(cls):
        with cls._engine.connect() as conn:
            print(conn.execute(cls.keys.select().where(cls.keys.c.id == 1)).fetchone())



db_sql = SQLAlchemyForKeys()

# db_sql.insert_keys(aws_access_key_id, aws_secret_access_key, key)
db_sql.get_keys()
    


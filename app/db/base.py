from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# This file is used to import all the models so that Alembic can access the metadata for migrations. 
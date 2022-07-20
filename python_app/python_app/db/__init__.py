import os
from sqlalchemy import (create_engine, Column)

from sqlalchemy.dialects.mysql import INTEGER

from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.ext.mypy.names import COLUMN
from sqlalchemy.sql.expression import column
from sqlalchemy.sql import func
from alembic.ddl.base import ColumnNullable

mapper_registry = registry()
Base = mapper_registry.generate_base()

def open(settings, mode='rw'):
    connect_string = f'mysql+pymysql://{os.environ.get("mysql_user")}:{os.environ.get("mysql_pass")}@{os.environ.get("mysql_host")}:{os.environ.get("mysql_port")}/{os.environ.get("mysql_db")}'
    
    return settings.setdefault(
            f'engine_{os.environ.get("mysql_db")}',
            create_engine(connect_string, pool_recycle=3600)
        )

def close(settings):
    engine = settings.pop(f'engine_{os.environ.get("mysql_db")}',None)
    engine.dispose()
    

class BoilerplateMixin(object):
    def base_url(self):
        return "http://localhost:5001"
    
    def get(self, attr, default=None):
        return getattr(self, attr, default)
    
    @declared_attr
    def id(cls):
        return Column(INTEGER(unsigned=True), primary_key=True, autoincrement='auto')
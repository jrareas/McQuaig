from sqlalchemy import(
    Column,
    JSON,
    String,
    desc,
    Integer,
    DateTime,
    ForeignKey,
    Boolean
)

from . import (Base, BoilerplateMixin)

class Order(BoilerplateMixin, Base):
    __tablename__ = "order"
    
    name = Column(String(200))
    email = Column(String(200))
    status = Column(String(50))
    
    
    def to_dict(self):
        return {
                'id': self.id,
                'email': self.email,
                'name': self.name,
                'status': self.status,
                'assessment_url': f'{self.base_url()}/order/{self.id}',
            }
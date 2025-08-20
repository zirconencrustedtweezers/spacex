from sqlalchemy import Column, String, Integer, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Rocket(Base):
    __tablename__ = "rockets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    weight = Column(Integer, nullable=True)
    description = Column(String(1000), nullable=True)

    def __repr__(self):
        return f"<Rocket(name='{self.name}', type='{self.type}')"

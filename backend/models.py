from sqlalchemy import Column, String, Integer, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Rocket(Base):
    __tablename__ = "rockets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    year_built = Column(Integer, nullable=True)
    mission = Column(String(500), nullable=True)
    attempted_landings = Column(Integer, default=0)
    successful_landings = Column(Integer, default=0)

    def __repr__(self):
        return f"<Rocket(name='{self.name}', model='{self.model}', year_built={self.year_built})"

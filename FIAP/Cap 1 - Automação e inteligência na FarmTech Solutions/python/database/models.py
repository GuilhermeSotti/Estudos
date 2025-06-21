from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

Base = declarative_base()
class Reading(Base):
    __tablename__ = 'readings'
    id = Column(Integer, primary_key=True)
    data_hora = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    umidade = Column(Float, nullable=False)
    nutriente = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Reading(data_hora={self.data_hora}, umidade={self.umidade}, nutriente={self.nutriente})>"

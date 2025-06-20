from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))        # Ex: umidade, nutrientes, temperatura
    localizacao = Column(String(100))  # Ex: "Estufa 1", "Lavoura A"

    def __repr__(self):
        return f"<Sensor(id={self.id}, tipo={self.tipo}, localizacao={self.localizacao})>"


class Leitura(Base):
    __tablename__ = 'leituras'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    valor = Column(Float)
    data_hora = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Leitura(sensor_id={self.sensor_id}, valor={self.valor}, data_hora={self.data_hora})>"

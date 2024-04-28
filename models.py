from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, Boolean
from pydantic import BaseModel

from database import Base


class Item(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True,index=True)
    group = Column(String,index=True)
    temperature = Column(Float,index=True)
    timeStamp = Column(String, index=True)
    errorStatus = Column(Boolean,index=True)


class SensorTempHistory(Base):
    __tablename__ = "sensor_temp_history"
    id = Column(Integer, primary_key=True,index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    temperature = Column(Float)
    timeStamp = Column(String)

class SensorCreate(BaseModel):
    group: str

class SensorResponse(BaseModel):
    id: int
    temperature: float
    errorStatus: bool

class SensorUpdate(BaseModel):
     new_group: str

class SensorDelete(BaseModel):
    id: int

class SensorTemp(BaseModel):
    temperature: float# | None = None
    timeStamp: str# | None = None

class SensorErrorUpdate(BaseModel):
    errorStatus: bool

class SensorTempsResponse(BaseModel):
    id: int
# AnturiAPI
 
Tarvitaan seuraavat python paketit:
fastapi
pydantic
sqlalchemy
uvicorn

## HUOM!
### Jotta virtuaaliympäristö toimii on oltava ./lopputyö/AnturiAPI kansiossa!




from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, Boolean
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import time
import random
import datetime

#FastAPI instanssi
app = FastAPI()

#Database
DATABASE_URL = "sqlite:///./sensor.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = sqlalchemy.orm.declarative_base()

#Database model
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

# Create table
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
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
# @app.get("/")
# def root():
#     return {"message": "Hello World!"}

# API endpoint to create an item
@app.post("/items/", response_model=SensorResponse)
async def create_item(item: SensorCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump()) #item.dict
    db_item.errorStatus = False
    newinfo = GenerateNewTemp()
    db_item.temperature = newinfo[0]
    db_item.timeStamp = newinfo[1]
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
 
 
# API endpoint to read an item by ID
@app.get("/items/{item_id}", response_model=SensorResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# API endpoint to change Sensor group
@app.patch("/items/{item_id}", response_model=SensorResponse)
async def update_item(item_id: int, item: SensorUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.group = item.new_group
    db.commit()
    db.refresh(db_item)
    return db_item

# Set new temp
@app.patch("/items/update/{item_id}", response_model=SensorTemp)
async def update_temp(item_id: int, item: SensorTemp, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    newInfo = GenerateNewTemp()
    newTemp = newInfo[0]

    db_item.temperature = newTemp
    db_item.timeStamp = str(datetime.datetime.now())

    # Create and add new SensorTempHistory entry
    new_history_entry = SensorTempHistory(
        sensor_id=db_item.id,
        temperature=db_item.temperature,
        timeStamp=db_item.timeStamp
    )
    db.add(new_history_entry)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.patch("/items/{item_id}/error", response_model=SensorResponse)
async def update_error_status(item_id: int, item: SensorErrorUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.errorStatus = item.errorStatus
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}",response_model=SensorResponse)
async def delete_item(item_id: int, item: SensorDelete, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return db_item


def GenerateNewTemp():
    randomNum = random.Random()
    newTemp = float(randomNum.randint(18,26))
    timestamp = datetime.datetime.now()
    timestamp = str(timestamp)

    return newTemp, timestamp

#Temphistory column
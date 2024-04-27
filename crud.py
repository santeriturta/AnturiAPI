from fastapi import APIRouter, Depends, HTTPException
from models import Item, SensorTempHistory, SensorCreate, SensorDelete, SensorErrorUpdate, SensorResponse, SensorTemp, SensorUpdate
from database import get_db  # Import get_db function from database.py
from pydantic import BaseModel
import datetime
from utils import GenerateNewTemp  # Import GenerateNewTemp from utils.py
from database import Session  # Import Session from database.py


router = APIRouter()


def get_sensor_data(db: Session, sensor_id: int):
  """
  Fetches sensor data by ID from the database.

  Args:
      db: Injected database session dependency.
      sensor_id: ID of the sensor to retrieve data for.

  Returns:
      The sensor data object from the database, or None if not found.
  """
  sensor_item = db.query(Item).filter(Item.id == sensor_id).first()
  return sensor_item


@router.post("/items/", response_model=SensorResponse)
async def create_item(item: SensorCreate, db: Session = Depends(get_db)):
  """
  API endpoint to create a new sensor entry.

  Args:
      item: Sensor data to create in the database.
      db: Injected database session dependency.

  Returns:
      The created sensor data object.
  """
  db_item = Item(**item.model_dump())
  db_item.errorStatus = False
  newinfo = GenerateNewTemp()
  db_item.temperature = newinfo[0]
  db_item.timeStamp = newinfo[1]
  db.add(db_item)
  db.commit()
  db.refresh(db_item)
  return db_item


@router.get("/items/{item_id}", response_model=SensorResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
  """
  API endpoint to read an item (sensor data) by ID.

  Raises:
      HTTPException: 404 Not Found if the sensor is not found.
  """
  db_item = get_sensor_data(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")
  return db_item


@router.patch("/items/{item_id}", response_model=SensorResponse)
async def update_item(item_id: int, item: SensorUpdate, db: Session = Depends(get_db)):
  """
  API endpoint to change sensor group.

  Raises:
      HTTPException: 404 Not Found if the sensor is not found.
  """
  db_item = get_sensor_data(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")

  db_item.group = item.new_group
  db.commit()
  db.refresh(db_item)
  return db_item


@router.patch("/items/update/{item_id}", response_model=SensorTemp)
async def update_temp(item_id: int, item: SensorTemp, db: Session = Depends(get_db)):
  """
  API endpoint to update sensor temperature and create a history entry.

  Raises:
      HTTPException: 404 Not Found if the sensor is not found.
  """
  db_item = get_sensor_data(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")

  new_temp = GenerateNewTemp()

  db_item.temperature = new_temp[0]
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


@router.patch("/items/{item_id}/error", response_model=SensorResponse)
async def update_error_status(item_id: int, item: SensorErrorUpdate, db: Session = Depends(get_db)):
  """
  API endpoint to update sensor error status.

  Raises:
      HTTPException: 404 Not Found if the sensor is not found.
  """
  db_item = get_sensor_data(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")

  db_item.errorStatus = item.errorStatus
  db.commit()
  db.refresh(db_item)
  return db_item


@router.delete("/items/{item_id}", response_model=SensorResponse)
async def delete_item(item_id: int, item: SensorDelete, db: Session = Depends(get_db)):
  """
  API endpoint to delete a sensor entry.

  Raises:
      HTTPException: 404 Not Found if the sensor is not found.
  """
  db_item = get_sensor_data(db, item_id)
  if db_item is None:
    raise HTTPException(status_code=404, detail="Item not found")

  db.delete(db_item)
  db.commit()
  return db_item

#app.include_router(router)
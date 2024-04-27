from pydantic import BaseModel
from fastapi import FastAPI
from models import Item, SensorCreate,SensorDelete,SensorErrorUpdate,SensorResponse,SensorTemp,SensorTempHistory,SensorUpdate
from database import engine
from crud import router
from utils import GenerateNewTemp

Item.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/sensors")

from pydantic import BaseModel
from enum import Enum

class Flight(BaseModel):
    flight_num: str
    capacity: int
    estimated_flight_duration: int

class Airline(str, Enum):
   DELTA = "Delta"
   SOUTHWEST = "Southwest"
   ALASKA = "Alaska"
   
class Update_Flight(BaseModel):
    capacity: int
    estimated_flight_duration: int

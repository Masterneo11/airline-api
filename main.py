from fastapi import FastAPI, HTTPException
import json
from models import Flight, Airline, Update_Flight

app = FastAPI()

with open("airlines.json", "r") as f:
    data = json.load(f)

airlines:dict[Airline, list[Flight]] = {}
for key, value in data.items():
    airlines[Airline[key.upper()]] = []
    # airlines[Airline.__dict__[key]] 
    for flight in value:
        flights_from_airlines = Flight(name=key, flight_num=flight["flight_num"], capacity=flight["capacity"], estimated_flight_duration=flight["estimated_flight_duration"])
        airlines[Airline[key.upper()]].append(flights_from_airlines)

@app.get("/")
async def get_airline_names() -> list[Airline]:
    return list(airlines.keys())

@app.get("/{airline_name}")
async def get_flight_number(airline_name: Airline) -> list[str]:
    flight_numbers_from_airlines = []
    flights = airlines[airline_name]
    for index in flights:
        flight_numbers_from_airlines.append(index.flight_num)
    return flight_numbers_from_airlines
    
@app.get("/{airline_name}/{flight_num}")
async def get_flight_number(airline_name: Airline, flight_num : str) -> Flight:
        flights = airlines[airline_name]
        for index in flights:
            if flight_num == index.flight_num:
                return index
        raise HTTPException(status_code=404, detail="Flight doesnt exist")

@app.post("/airline")
async def create_airline(airline: Airline, flight: Flight):
    airlines[airline].append(flight)
    return "creating airline flight complete"

    
@app.put("/{airline}/{flight_num}")
async def update_flight(airline: Airline, flight_num: str, update_flight: Update_Flight):
    flight_found = False
    for flight in airlines[airline]:
        if flight.flight_num == flight_num:
            flight_found = True
            flight.capacity = update_flight.capacity
            flight.estimated_flight_duration = update_flight.estimated_flight_duration
            break
    if not flight_found:
        new_flight = Flight(flight_num=flight_num,
                            capacity=update_flight.capacity,
                            estimated_flight_duration=update_flight.estimated_flight_duration)
        airlines[airline].append(new_flight)
    return "Flight updated successfully"


@app.delete("/{airline}/{fligh_num}")
async def delete_flight_number_from_airline(airline: Airline, flight_num: str,):
    for index in airlines[airline]:
        if flight_num == index.flight_num:
           airlines[airline].remove(index)
    return "flight has been deleted from flights"

"""
Have these endpoints:
GET / -> list[airline_name]    
GET /:airline_name -> list[flight_num]    just the flight_num from the dict in the list
GET /:airline_name/:flight_num -> Flight   just the one flight from the list of dictionaries

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num

"""



from fastapi import FastAPI, HTTPException
import json
from models import Flight, Airline

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
async def update_flights(airline: Airline, flight_num: str, new_flight: Flight):
    flights = airlines[airline]
    for index, flight in enumerate(flights):
        if flight_num == flight.flight_num:
            if new_flight.capacity is not None:
                flights[index].capacity = new_flight.capacity
            if new_flight.estimated_flight_duration is not None:
                flights[index].estimated_flight_duration = new_flight.estimated_flight_duration
            if new_flight.flight_num is not None:
                flights[index].flight_num = new_flight.flight_num
            return " flight updated"
    
            


@app.delete("/{airline}/{fligh_num}")
async def delete_flight_number_from_airline(airline: Airline, flight_num: str,):
    flights = airlines[airline]
    for index in flights:
        if flight_num == index.flight_num:
           flights.remove(index)
           return "flight has been deleted from flights"
    return " That flight does not exist"

"""
Have these endpoints:
GET / -> list[airline_name]    
GET /:airline_name -> list[flight_num]    just the flight_num from the dict in the list
GET /:airline_name/:flight_num -> Flight   just the one flight from the list of dictionaries

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num

"""



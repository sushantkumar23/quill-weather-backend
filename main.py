# main.py
import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

WEATHERSTACK_API_KEY = os.getenv('WEATHERSTACK_API_KEY')
WEATHERSTACK_BASE_URL = 'http://api.weatherstack.com/current'

app = FastAPI(title="Quill Weather API")

origins = [
    "http://localhost:3000",
    "https://quill-weather.vercel.app",
    "https://quill-weather-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/weather")
def get_weather(location: str):
    params = {
        'access_key': WEATHERSTACK_API_KEY,
        'query': location,
        'forecast_days': 1,
        'hourly': 1
    }
    response = requests.get(WEATHERSTACK_BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("data: ", data)
        if 'current' in data:
            return data
        else:
            raise HTTPException(status_code=404, detail="Weather information not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

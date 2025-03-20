# models.py
from pydantic import BaseModel
from typing import List, Dict

class AttendanceRequest(BaseModel):
    home_div: int
    away_div: int
    fan_base_home: int
    fan_base_away: int
    morale_home: float
    morale_away: float
    rating_home: int
    rating_away: int
    weather: str
    match_format: str

class AttendanceResponse(BaseModel):
    category: str
    attendance: int

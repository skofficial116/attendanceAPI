# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from models import AttendanceRequest, AttendanceResponse
from calculateAttendance import calculate_attendance
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list of allowed domains like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "FastAPI is deployed on Render!"}


@app.post("/calculate_attendance/", response_model=List[AttendanceResponse])
def get_attendance(data: AttendanceRequest):
    """
    API endpoint to get attendance predictions.
    """

    try:
        # Call the function from attendance.py
        attendance_data = calculate_attendance(
            data.home_div,
            data.away_div,
            data.fan_base_home,
            data.fan_base_away,
            data.morale_home,
            data.morale_away,
            data.rating_home,
            data.rating_away,
            data.weather,
            data.match_format,
        )
        return attendance_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

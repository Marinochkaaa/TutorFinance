from fastapi import FastAPI
from pydantic import BaseModel
from salary import calculate_salary
from fastapi.responses import JSONResponse
import json
from pathlib import Path
from analytics import calculate_analytics

app = FastAPI(title="TutorFinance API")

class SalaryRequest(BaseModel):
    teacherId: int
    year: int
    month: int

@app.get("/")
def home():
    return JSONResponse(
        content={"message": "Добро пожаловать в TutorFinance!"},
        media_type="application/json; charset=utf-8"
    )

@app.get("/api/teachers")
def get_teachers():
    file_path = Path(__file__).parent / "Data" / "teachers.json"

    with open(file_path, "r", encoding="utf-8") as file:
        teachers = json.load(file)

    return JSONResponse(
    content=teachers,
    media_type="application/json; charset=utf-8"
    )

@app.post("/api/salary/calculate")
def calculate(request: SalaryRequest):
    result = calculate_salary(
        request.teacherId,
        request.year,
        request.month
    )

    return JSONResponse(
        content=result,
        media_type="application/json; charset=utf-8"
    )


@app.get("/api/analytics")
def get_analytics(year: int, month: int):
    result = calculate_analytics(year, month)

    return JSONResponse(
        content=result,
        media_type="application/json; charset=utf-8"
    )

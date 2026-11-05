
import json
from pathlib import Path
from salary import calculate_salary


def calculate_analytics(year, month):
    data_folder = Path(__file__).parent / "Data"

    with open(data_folder / "teachers.json", encoding="utf-8") as file:
        teachers = json.load(file)

    total_amount = 0
    teachers_count = 0

    for teacher in teachers:
        result = calculate_salary(
            teacher["teacherId"],
            year,
            month
        )

        if "error" in result:
            return result

        if result["lessonsTotal"] > 0:
            total_amount += result["finalAmount"]
            teachers_count += 1

    if teachers_count > 0:
        average_amount = round(total_amount / teachers_count, 2)
    else:
        average_amount = 0

    return {
        "period": f"{month:02d}.{year}",
        "teachersCount": teachers_count,
        "totalAmount": round(total_amount, 2),
        "averageAmount": average_amount,
        "currency": "RUB"
    }

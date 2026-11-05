import json
from pathlib import Path
from currency import get_exchange_rate


def calculate_salary(teacher_id, year, month):
    data_folder = Path(__file__).parent / "Data"

    with open(data_folder / "teachers.json", encoding="utf-8") as file:
        teachers = json.load(file)

    with open(data_folder / "lessons.json", encoding="utf-8") as file:
        lessons = json.load(file)

    teacher = next(
        (t for t in teachers if t["teacherId"] == teacher_id),
        None
    )

    if teacher is None:
        return {"error": "Преподаватель не найден"}

    selected_lessons = [
        lesson for lesson in lessons
        if lesson["teacherId"] == teacher_id
        and lesson["date"].startswith(f"{year}-{month:02d}-")
    ]

 
    base_amount = 0

    for lesson in selected_lessons:
        try:
            exchange_rate = get_exchange_rate(
                lesson["currency"],
                lesson["date"]
            )
        except Exception as error:
            return {
                "error": f"Не удалось получить курс валюты: {error}"
            }

        lesson_cost = (
            lesson["hourRate"]
            * exchange_rate
            * lesson["duration"]
            * lesson["paymentCoefficient"]
        )

        base_amount += lesson_cost


    p = teacher["deductionCoefficient"]
    deduction_amount = round(base_amount * p, 2)
    final_amount = round(base_amount - deduction_amount, 2)

    return {
        "teacherId": teacher_id,
        "teacherName": teacher["fullName"],
        "period": f"{month:02d}.{year}",
        "lessonsTotal": len(selected_lessons),
        "lessonsConducted": sum(
            1 for lesson in selected_lessons
            if lesson["status"] == "Проведено"
        ),
        "lessonsMissed": sum(
            1 for lesson in selected_lessons
            if lesson["status"] == "Пропущено"
        ),
        "baseAmount": round(base_amount, 2),
        "deductionCoefficient": p,
        "deductionAmount": deduction_amount,
        "finalAmount": final_amount,
        "currency": "RUB"
    }
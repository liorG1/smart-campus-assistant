from sqlalchemy.orm import Session

from app.crud.buildings import search_buildings
from app.crud.campus_info import search_campus_info
from app.crud.courses import search_courses
from app.crud.exam_schedules import (
    get_exam_schedules_by_course_code,
    get_exam_schedules_by_course_name,
)
from app.crud.office_hours import (
    get_office_hours_by_office_name,
    get_office_hours_by_staff_name,
    search_office_hours,
)
from app.crud.rooms import search_rooms
from app.crud.technical_issues import search_technical_issues


def _dedupe_by_id(records):
    unique_records = []
    seen_ids = set()
    for record in records:
        if record.id not in seen_ids:
            seen_ids.add(record.id)
            unique_records.append(record)
    return unique_records


def _format_exam_results(exams) -> str:
    lines = []
    for exam in exams:
        room_text = "Room not assigned"
        if exam.room:
            building_name = exam.room.building.name if exam.room.building else "Unknown building"
            room_text = f"{building_name}, room {exam.room.room_number}"

        lines.append(
            f"- Course: {exam.course.course_name} ({exam.course.course_code}), "
            f"Date: {exam.exam_date}, Time: {exam.exam_time}, "
            f"Location: {room_text}, Notes: {exam.notes or 'None'}"
        )
    return "\n".join(lines)


def _format_location_results(buildings, rooms) -> str:
    lines = []

    for building in buildings:
        lines.append(
            f"- Building: {building.name}, Code: {building.code or 'N/A'}, "
            f"Address: {building.address or 'N/A'}, Description: {building.description or 'N/A'}"
        )

    for room in rooms:
        building_name = room.building.name if room.building else "Unknown building"
        lines.append(
            f"- Room: {room.room_number}, Building: {building_name}, "
            f"Floor: {room.floor if room.floor is not None else 'N/A'}, "
            f"Description: {room.description or 'N/A'}"
        )

    return "\n".join(lines)


def _format_office_hours_results(records) -> str:
    lines = []
    for record in records:
        building_name = record.building.name if record.building else "N/A"
        room_number = record.room.room_number if record.room else "N/A"

        lines.append(
            f"- Staff: {record.staff_name}, Office: {record.office_name or 'N/A'}, "
            f"Day: {record.day_of_week}, Start: {record.start_time}, End: {record.end_time}, "
            f"Building: {building_name}, Room: {room_number}, Notes: {record.notes or 'None'}"
        )

    return "\n".join(lines)


def _format_campus_info_results(records) -> str:
    lines = []
    for record in records:
        lines.append(
            f"- Title: {record.title}, Category: {record.category}, Content: {record.content}"
        )
    return "\n".join(lines)


def _format_technical_issue_results(records) -> str:
    lines = []
    for record in records:
        lines.append(
            f"- Problem: {record.problem}, Category: {record.category or 'N/A'}, "
            f"Solution: {record.solution}, Notes: {record.notes or 'None'}"
        )
    return "\n".join(lines)


def get_exam_context(db: Session, question: str, entities: dict | None = None) -> str | None:
    entities = entities or {}
    course_name = entities.get("course_name")

    exams = []
    if course_name:
        exams.extend(get_exam_schedules_by_course_name(db, course_name))
        exams.extend(get_exam_schedules_by_course_code(db, course_name))

    if not exams:
        courses = search_courses(db, question)
        for course in courses:
            exams.extend(get_exam_schedules_by_course_code(db, course.course_code))
            exams.extend(get_exam_schedules_by_course_name(db, course.course_name))

    if not exams:
        exams = get_exam_schedules_by_course_code(db, question)
    if not exams:
        exams = get_exam_schedules_by_course_name(db, question)

    exams = _dedupe_by_id(exams)
    if not exams:
        return None
    return _format_exam_results(exams[:5])


def get_location_context(db: Session, question: str, entities: dict | None = None) -> str | None:
    entities = entities or {}
    building_name = entities.get("building_name")
    room_number = entities.get("room_number")

    buildings = search_buildings(db, building_name) if building_name else []
    rooms = search_rooms(db, room_number) if room_number else []

    if not buildings and not rooms:
        buildings = search_buildings(db, question)
        rooms = search_rooms(db, question)

    if not buildings and not rooms:
        return None

    return _format_location_results(buildings[:5], rooms[:5])


def get_office_hours_context(db: Session, question: str, entities: dict | None = None) -> str | None:
    entities = entities or {}
    staff_name = entities.get("staff_name")

    records = []
    if staff_name:
        records.extend(get_office_hours_by_staff_name(db, staff_name))

    if not records:
        records.extend(get_office_hours_by_office_name(db, question))
        records.extend(search_office_hours(db, question))

    records = _dedupe_by_id(records)
    if not records:
        return None
    return _format_office_hours_results(records[:5])


def get_general_info_context(db: Session, question: str, entities: dict | None = None) -> str | None:
    entities = entities or {}
    service_name = entities.get("service_name")

    records = search_campus_info(db, service_name) if service_name else search_campus_info(db, question)
    if not records:
        return None
    return _format_campus_info_results(records[:5])


def get_technical_problem_context(db: Session, question: str, entities: dict | None = None) -> str | None:
    entities = entities or {}
    technical_issue = entities.get("technical_issue")

    records = search_technical_issues(db, technical_issue) if technical_issue else search_technical_issues(db, question)
    if not records:
        return None
    return _format_technical_issue_results(records[:5])


def get_context_by_category(db: Session, category: str, question: str, entities: dict | None = None) -> str | None:
    if category == "exam":
        return get_exam_context(db, question, entities)
    if category == "location":
        return get_location_context(db, question, entities)
    if category == "office_hours":
        return get_office_hours_context(db, question, entities)
    if category == "general_info":
        return get_general_info_context(db, question, entities)
    if category == "technical_problem":
        return get_technical_problem_context(db, question, entities)
    return None

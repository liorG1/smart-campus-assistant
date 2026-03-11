from datetime import date, time

from app import models
from app.db import Base, SessionLocal, engine


def reset_tables(db):
    db.query(models.ExamSchedule).delete()
    db.query(models.OfficeHours).delete()
    db.query(models.Room).delete()
    db.query(models.Course).delete()
    db.query(models.Building).delete()
    db.query(models.CampusInfo).delete()
    db.query(models.TechnicalIssue).delete()
    db.commit()


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("Seeding database...")
    reset_tables(db)

    engineering = models.Building(
        name="Engineering Building",
        code="ENG",
        address="North Campus",
        description="Main engineering classrooms",
    )
    science = models.Building(
        name="Science Building",
        code="SCI",
        address="West Campus",
        description="Science laboratories",
    )
    library_building = models.Building(
        name="Central Library",
        code="LIB",
        address="Main Campus",
        description="Campus main library",
    )
    admin_building = models.Building(
        name="Student Services Center",
        code="SSC",
        address="East Campus",
        description="Administrative and student support offices",
    )
    db.add_all([engineering, science, library_building, admin_building])
    db.commit()

    room1 = models.Room(building_id=engineering.id, room_number="210", floor=2, description="Computer science classroom")
    room2 = models.Room(building_id=engineering.id, room_number="305", floor=3, description="Large lecture hall")
    room3 = models.Room(building_id=science.id, room_number="101", floor=1, description="Physics lab")
    room4 = models.Room(building_id=admin_building.id, room_number="12", floor=1, description="Student reception office")
    db.add_all([room1, room2, room3, room4])
    db.commit()

    ds = models.Course(course_code="CS201", course_name="Data Structures")
    os_course = models.Course(course_code="CS301", course_name="Operating Systems")
    calc = models.Course(course_code="MATH101", course_name="Calculus 1")
    ai_course = models.Course(course_code="CS410", course_name="Introduction to Artificial Intelligence")
    db.add_all([ds, os_course, calc, ai_course])
    db.commit()

    exams = [
        models.ExamSchedule(course_id=ds.id, exam_date=date(2026, 3, 20), exam_time=time(9, 0), room_id=room1.id, notes="Final exam"),
        models.ExamSchedule(course_id=os_course.id, exam_date=date(2026, 3, 25), exam_time=time(13, 0), room_id=room2.id, notes="Semester exam"),
        models.ExamSchedule(course_id=calc.id, exam_date=date(2026, 3, 28), exam_time=time(10, 30), room_id=room3.id, notes=None),
        models.ExamSchedule(course_id=ai_course.id, exam_date=date(2026, 4, 2), exam_time=time(11, 0), room_id=room2.id, notes="Bring student ID"),
    ]
    db.add_all(exams)
    db.commit()

    office_hours = [
        models.OfficeHours(
            staff_name="Dr. Cohen",
            office_name="Computer Science Office",
            day_of_week="Sunday",
            start_time=time(10, 0),
            end_time=time(12, 0),
            building_id=engineering.id,
            room_id=room1.id,
            notes="Student consultation",
        ),
        models.OfficeHours(
            staff_name="Prof. Levy",
            office_name="Math Department",
            day_of_week="Tuesday",
            start_time=time(14, 0),
            end_time=time(16, 0),
            building_id=science.id,
            room_id=room3.id,
            notes=None,
        ),
        models.OfficeHours(
            staff_name="Student Services Desk",
            office_name="Student Reception",
            day_of_week="Monday",
            start_time=time(9, 0),
            end_time=time(15, 0),
            building_id=admin_building.id,
            room_id=room4.id,
            notes="For enrollment and official documents",
        ),
    ]
    db.add_all(office_hours)
    db.commit()

    campus_info = [
        models.CampusInfo(
            title="Library Hours",
            category="service",
            content="The campus library is open Sunday to Thursday from 08:00 to 22:00.",
        ),
        models.CampusInfo(
            title="Campus WiFi",
            category="service",
            content="Students can connect to CampusNet using their student credentials.",
        ),
        models.CampusInfo(
            title="Parking",
            category="facility",
            content="Student parking is available in Lot A and Lot B.",
        ),
        models.CampusInfo(
            title="Cafeteria Hours",
            category="service",
            content="The cafeteria is open Sunday to Thursday from 07:30 to 18:00.",
        ),
        models.CampusInfo(
            title="Student Office",
            category="service",
            content="The student office is located in the Student Services Center, room 12.",
        ),
    ]
    db.add_all(campus_info)
    db.commit()

    technical_issues = [
        models.TechnicalIssue(
            problem="Cannot connect to campus wifi",
            category="wifi",
            solution="Select the CampusNet network and log in with your student username and password.",
            notes="Restart the device if the problem continues.",
        ),
        models.TechnicalIssue(
            problem="Cannot log in to Moodle",
            category="portal",
            solution="Reset your campus password and clear your browser cache before trying again.",
            notes="If the problem continues, contact IT support.",
        ),
        models.TechnicalIssue(
            problem="Student portal page not loading",
            category="portal",
            solution="Refresh the page, clear browser cache, and try another browser.",
            notes="If unavailable for more than 30 minutes, contact the help desk.",
        ),
    ]
    db.add_all(technical_issues)
    db.commit()

    db.close()
    print("Seed completed successfully!")


if __name__ == "__main__":
    seed()

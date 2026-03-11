from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AdminBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    is_active: bool = True


class AdminCreate(AdminBase):
    password: str = Field(min_length=6, max_length=100)


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminRead(AdminBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    admin: AdminRead
    access_token: str
    token_type: str = "bearer"


class BuildingBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    code: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    code: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None


class BuildingRead(BuildingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class RoomBase(BaseModel):
    building_id: int
    room_number: str = Field(min_length=1, max_length=20)
    floor: Optional[int] = None
    description: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    building_id: Optional[int] = None
    room_number: Optional[str] = Field(default=None, min_length=1, max_length=20)
    floor: Optional[int] = None
    description: Optional[str] = None


class RoomRead(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    course_code: str = Field(min_length=1, max_length=30)
    course_name: str = Field(min_length=1, max_length=150)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    course_code: Optional[str] = Field(default=None, min_length=1, max_length=30)
    course_name: Optional[str] = Field(default=None, min_length=1, max_length=150)


class CourseRead(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ExamScheduleBase(BaseModel):
    course_id: int
    exam_date: date
    exam_time: time
    room_id: Optional[int] = None
    notes: Optional[str] = None


class ExamScheduleCreate(ExamScheduleBase):
    pass


class ExamScheduleUpdate(BaseModel):
    course_id: Optional[int] = None
    exam_date: Optional[date] = None
    exam_time: Optional[time] = None
    room_id: Optional[int] = None
    notes: Optional[str] = None


class ExamScheduleRead(ExamScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class OfficeHoursBase(BaseModel):
    office_name: Optional[str] = Field(default=None, max_length=120)
    staff_name: str = Field(min_length=1, max_length=120)
    day_of_week: str = Field(min_length=1, max_length=20)
    start_time: time
    end_time: time
    building_id: Optional[int] = None
    room_id: Optional[int] = None
    notes: Optional[str] = None


class OfficeHoursCreate(OfficeHoursBase):
    pass


class OfficeHoursUpdate(BaseModel):
    office_name: Optional[str] = Field(default=None, max_length=120)
    staff_name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    day_of_week: Optional[str] = Field(default=None, min_length=1, max_length=20)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    building_id: Optional[int] = None
    room_id: Optional[int] = None
    notes: Optional[str] = None


class OfficeHoursRead(OfficeHoursBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CampusInfoBase(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    category: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1)


class CampusInfoCreate(CampusInfoBase):
    pass


class CampusInfoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    category: Optional[str] = Field(default=None, min_length=1, max_length=50)
    content: Optional[str] = Field(default=None, min_length=1)


class CampusInfoRead(CampusInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TechnicalIssueBase(BaseModel):
    problem: str = Field(min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=50)
    solution: str = Field(min_length=1)
    notes: Optional[str] = None


class TechnicalIssueCreate(TechnicalIssueBase):
    pass


class TechnicalIssueUpdate(BaseModel):
    problem: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, max_length=50)
    solution: Optional[str] = Field(default=None, min_length=1)
    notes: Optional[str] = None


class TechnicalIssueRead(TechnicalIssueBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)


class AskResponse(BaseModel):
    category: Optional[str] = None
    answer: str
    source: Optional[str] = None

from pydantic import BaseModel
from datetime import datetime


class GroupStudentBase(BaseModel):
    student: "StudentGroupInfo"
    join_date: datetime

    class Config:
        from_attributes = True


class GroupTeacherBase(BaseModel):
    teacher: "TeacherGroupInfo"

    class Config:
        from_attributes = True


class MemberGroupBase(BaseModel):
    group: "GroupBaseInfo"

    class Config:
        from_attributes = True


from app.schemas.group import GroupBaseInfo
from app.schemas.student import StudentGroupInfo
from app.schemas.teacher import TeacherGroupInfo

GroupStudentBase.model_rebuild()
GroupTeacherBase.model_rebuild()
MemberGroupBase.model_rebuild()

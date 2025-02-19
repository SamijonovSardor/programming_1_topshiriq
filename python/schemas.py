from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

class BranchCreate(BaseModel):
    name: str

class GroupCreate(BaseModel):
    name: str
    branch_id: int

class StudentCreate(BaseModel):
    name: str
    group_id: int

class TeacherCreate(BaseModel):
    name: str
    group_id: int
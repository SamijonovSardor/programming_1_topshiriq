from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
from models import User, Branch, Group, Student, Teacher
from schemas import GroupCreate, UserCreate, UserResponse, BranchCreate, StudentCreate, TeacherCreate
from auth import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, get_user

app = FastAPI()

# Database va modellarning o'zaro aloqasini o'rnatish
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = get_user(db, form_data.username)
    
#     # Foydalanuvchini tekshirish
#     if not user or user.password != form_data.password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     access_token = create_access_token(data={"sub": user.username, "role": user.role})
#     return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
def login (user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Teacher endpointlari
@app.get("/teacher/groups")
def get_teacher_groups(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Group).filter(Group.id == current_user['group_id']).all()

@app.get("/teacher/students")
def get_students_in_group(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Student).filter(Student.group_id == current_user['group_id']).all()

# Admin endpointlari
@app.get("/admin/groups")
def list_groups(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Group).all()

@app.get("/admin/teachers")
def list_teachers(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Teacher).all()

@app.get("/admin/students")
def list_students(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Student).all()

@app.post("/admin/add_student", response_model=StudentCreate)
def add_student(student: StudentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_student = Student(name=student.name, group_id=student.group_id)
    db.add(db_student)
    db.commit()
    return db_student

@app.post("/admin/add_teacher", response_model=TeacherCreate)
def add_teacher(teacher: TeacherCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_teacher = Teacher(name=teacher.name, group_id=teacher.group_id)
    db.add(db_teacher)
    db.commit()
    return db_teacher

@app.post("/admin/add_group", response_model=GroupCreate)
def add_group(group: GroupCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_group = Group(name=group.name, branch_id=group.branch_id)
    db.add(db_group)
    db.commit()
    return db_group

# Superadmin endpointlari
@app.post("/superadmin/add_admin")
def add_admin(user: UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    db_user = User(username=user.username, password=user.password, role='admin')
    db.add(db_user)
    db.commit()
    return db_user

@app.get("/superadmin/all_students")
def list_all_students(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Student).all()

@app.get("/superadmin/all_groups")
def list_all_groups(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Group).all()

@app.get("/superadmin/all_teachers")
def list_all_teachers(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Teacher).all()
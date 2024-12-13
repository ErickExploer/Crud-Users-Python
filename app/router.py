from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import UserSchema, RequestUser, Response  # Cambio de BookSchema a UserSchema
import crud
from config import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo usuario
@router.post("/create")
async def create(user: UserSchema, db: Session = Depends(get_db)):
    if not user.first_name or not user.last_name or not user.dni:
        raise HTTPException(status_code=400, detail="First name, last name and DNI are required")

    created_user = crud.create_user(db, user)
    result = UserSchema.from_orm(created_user).dict(exclude_none=True)
    return Response(code="200", status="OK", message="User created", result=[result]).dict(exclude_none=True)

# Obtener todos los usuarios
@router.get("/")
async def get(db: Session = Depends(get_db)):
    _users = crud.get_users(db)
    result = [UserSchema.from_orm(user).dict() for user in _users]
    return Response(code="200", status="OK", message="Success Fetch", result=result).dict(exclude_none=True)

# Obtener usuario por ID
@router.get("/{user_id}")
async def get_by_id(user_id: int, db: Session = Depends(get_db)):
    _user = crud.get_user_by_id(db, user_id)
    if _user is None:
        raise HTTPException(status_code=404, detail="User not found")
    result = UserSchema.from_orm(_user).dict()
    return Response(code="200", status="OK", message="Success get data", result=[result]).dict(exclude_none=True)

# Actualizar usuario
@router.post("/update")
async def update_user(request: RequestUser, db: Session = Depends(get_db)):
    _user = crud.update_user(
        db,
        user_id=request.parameter.id,
        first_name=request.parameter.first_name,
        last_name=request.parameter.last_name,
        dni=request.parameter.dni,
        age=request.parameter.age,
        email=request.parameter.email
    )
    result = UserSchema.from_orm(_user).dict()
    return Response(code="200", status="OK", message="Success update", result=[result])

# Eliminar usuario
@router.delete("/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    _user = crud.get_user_by_id(db, id)
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.remove_user(db, user_id=id)
    return Response(code="200", status="OK", message="Successful delete").dict(exclude_none=True)
from sqlalchemy.orm import Session
from model import User  # Cambié Book a User, ya que estamos trabajando con la tabla de usuarios
from schemas import UserSchema


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserSchema):
    # Aquí, ajusté para que se utilicen los campos correctos (first_name, last_name, dni, age, email)
    _user = User(
        first_name=user.first_name, 
        last_name=user.last_name, 
        dni=user.dni, 
        age=user.age, 
        email=user.email
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)  # Asegura que la entidad esté actualizada después de commit
    return _user


def remove_user(db: Session, user_id: int):
    _user = get_user_by_id(db, user_id)
    if _user:
        db.delete(_user)
        db.commit()  # Eliminar usuario después de la consulta exitosa
    else:
        raise ValueError("User not found")  # Lanzar error si no se encuentra el usuario


def update_user(db: Session, user_id: int, first_name: str, last_name: str, dni: str, age: int, email: str):
    _user = get_user_by_id(db, user_id)
    
    if not _user:
        raise ValueError("User not found")  # Si no se encuentra el usuario, lanzamos un error
    
    # Actualizar los campos del usuario
    _user.first_name = first_name
    _user.last_name = last_name
    _user.dni = dni
    _user.age = age
    _user.email = email
    
    db.commit()  # Confirmar los cambios en la base de datos
    db.refresh(_user)  # Refrescar para obtener los datos actualizados
    return _user
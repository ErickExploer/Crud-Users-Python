from sqlalchemy import Column, Integer, String
from config import Base

class User(Base):
    __tablename__ = "users"  # Nombre de la tabla es 'users', como en tu base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único
    first_name = Column(String, nullable=False)  # Primer nombre, no puede ser nulo
    last_name = Column(String, nullable=False)  # Apellido, no puede ser nulo
    dni = Column(String, unique=True, nullable=False)  # DNI único, no puede ser nulo
    age = Column(Integer, nullable=False)  # Edad del usuario, no puede ser nulo
    email = Column(String, unique=True, nullable=False)  # Email único, no puede ser nulo
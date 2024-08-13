from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List
from typing import Optional
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Clase que me permite interactuar con la Base de Datos
Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25))
    fullname: Mapped[str] = mapped_column(String(80))
    password : Mapped[str] = mapped_column(String(128))
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
    
    def set_password(self, password_to_hash):
        self.password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_hash):
        return check_password_hash(self.password, password_to_hash)


class Task(Base):
    __tablename__ = 'tasks'
    id = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[Optional[str]] = mapped_column()
    fechaCreacion: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # fechaCreacion = mapped_column(DateTime, insert_default=datetime.now())
    
    user: Mapped["User"] = relationship(back_populates="tasks")


# Se instalan las librerias con flask_wtf y wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

# Clase para Login de User
class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='Por favor, introduce tu nombre de usuario.'),
        Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 caracteres.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Por favor, introduce tu contraseña.')
    ])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

# Clase para Registracion de User
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='Por favor, introduce tu nombre de usuario.'),
        Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 caracteres.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Por favor, introduce tu contraseña.'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
    ])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Por favor, confirma tu contraseña.'),
        EqualTo('password', message='Las contraseñas deben coincidir.')
    ])
    submit = SubmitField('Registrarse')
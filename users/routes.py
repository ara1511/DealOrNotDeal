from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models.models import User
from db import session
from config import var_globales

users_bp = Blueprint (
    "users_bp", __name__, template_folder="templates", static_folder="static"
)

#Ruta READ (Get)
@users_bp.route('/')
@login_required
def users():
    # users = [{'id':'1', 'name':'Daniel'}]
    # Mensaje en caso de que no haya ningun Registro (Fila)
    # Debo Mostrar los items en orden Descendente Por Nombre (name)
    users = session.query(User).all()
    return render_template('users/items.html', users=users)

# Ruta para mostrar un solo User
@users_bp.route('/<int:user_id>')
@login_required
def getuser(user_id):
    # Hacer el control de Errores
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        var_globales['mensaje'] = 'NO EXISTE EL USUARIO'
    return render_template('users/item.html', user=user)

# Rura para Crear un Usuario
# @users_bp.route('/create', methods=["GET", "POST"])
# def createuser():
#     # Lo primero que evaluo es que metodo esta llamando a la ruta
#     if request.method == 'POST':
#         # Dentro del REQUEST viene un FORM que es una coleccion de INPUT's que 
#         # deben tener en su propiedad "name" el nombre con el cual lo llamo para
#         # usarlo
#         name = request.form['username']
#         password = request.form['password']
#         # Creamos un Elemento de tipo de la clase que mapea a la tabla de la base de datos
#         user = User(name=name, password=password)
#         try:
#             # Agregamos el elmento creado
#             session.add(user)
#             # Guardo en la base de datos todos los elementos que se agregaron o modiforon
#             session.commit()
#             print('User Creado con Exito')
#         except Exception as e:
#             print(f'A courrido un error {e}')
#         if var_globales['isLogued']:
#             return redirect('/users')
#         return redirect('/')
#     else:
#         return render_template('users/create.html')

@users_bp.route('/delete/<int:user_id>')
@login_required
def deleteuser(user_id:int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        try:
            session.delete(user)
            session.commit()
        except Exception as e:
            print(f'Error al eliminar. {e}')
    return redirect('/users')

@users_bp.route('/edit/<int:user_id>', methods=["GET", "POST"])
@login_required
def edituser(user_id:int):
    # Lo primero que evaluo es que metodo esta llamando a la ruta
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if request.method == 'POST':
            # Dentro del REQUEST viene un FORM que es una coleccion de INPUT's que 
            # deben tener en su propiedad "name" el nombre con el cual lo llamo para
            # usarlo
            name = request.form['username']
            password = request.form['password']
            # Asignamos el contenido de la variables que vienen del FORM porque puedo 
            # hacer validaciones extras
            user.name = name
            user.password = password
            try:
                # Guardo en la base de datos todos los elementos que se agregaron o modiforon
                session.commit()
            except Exception as e:
                print(f'A courrido un error {e}')
            return redirect('/users')
        else:
            return render_template('users/edit.html', user=user)
from flask import Flask, render_template
from flask_login import LoginManager
from models.models import User
from werkzeug.exceptions import BadRequest, NotFound
import db

app = Flask(__name__)
app.config.from_object('config')

# Configuración de Flask Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')

# Registro de Blueprints
from main.routes import main_bp
from auth.routes import auth_bp
from users.routes import users_bp
from game.game_routes import game_bp

app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(game_bp, url_prefix='/games')


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400

@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('404.html')

from config import var_globales
@app.context_processor
def inject_variables():
    return var_globales

# Filtro personalizado para formatear la fecha
@app.template_filter('format_datetime')
def format_datetime(value, format="%d/%m/%Y %H:%M:%S"):
    return value.strftime(format)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])

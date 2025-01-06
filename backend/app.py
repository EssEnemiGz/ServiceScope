from flask import *
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv
import os

# Importing microservices
import services.render as render
import services.session as session

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
#app.config['SESSION_COOKIE_DOMAIN'] = ""
app.permanent_session_lifetime = timedelta(weeks=52) # Sesion con duracion de 52 semanas o 1 año
app.url_map.strict_slashes = False

CORS(app, origins=["*"])

# Importing micro services
app.register_blueprint(render.render_bp)
app.register_blueprint(session.session_bp)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/register')
def register_form():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
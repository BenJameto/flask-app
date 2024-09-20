import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
# Cargar diferentes archivos .env dependiendo del entorno
if os.getenv("FLASK_ENV") == "docker":
    load_dotenv(".env")  # Cargar el archivo para Docker
else:
    load_dotenv(".env.local")  # Cargar el archivo para local

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")  # Configura la clave secreta para sesiones

# Función para conectarse a la base de datos PostgreSQL
def get_db_connection():
    try:
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "hospitaldb")
        user = os.getenv("DB_USER", "hospitaluser")
        password = os.getenv("DB_PASSWORD", "hospitaluser1234")

        print(f"Conectando a la base de datos en {host}:{port}, database: {database}, user: {user}")

        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Conexión a la base de datos exitosa")
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


# Función para cerrar la conexión a la base de datos
def close_db_connection(conn):
    if conn is not None:
        conn.close()
        print("Conexión a la base de datos cerrada")

# Función para inicializar la base de datos desde el archivo SQL
def init_db():
    with app.app_context():
        conn = get_db_connection()
        if conn:
            c = conn.cursor()
            # Ejecutar el script SQL que creará las tablas
            try:
                with open('database/hospital.sql', 'r') as f:
                    sql_script = f.read()
                c.execute(sql_script)
                conn.commit()
                print("Base de datos inicializada correctamente")
            except Exception as e:
                print(f"Error al inicializar la base de datos: {e}")
            finally:
                close_db_connection(conn)

# Inicializar la base de datos cuando se inicie la aplicación
init_db()

#tuta principal> redirigir al inicio de sesion
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))

# Ruta para la página de inicio
@app.route('/home')
def home():
    conn = get_db_connection()
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Hospital")
        hospitales = c.fetchall()
        close_db_connection(conn)
        return render_template('home.html', hospitales=hospitales)
    else:
        return "Error al conectar con la base de datos"

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí podrías añadir la lógica para verificar el login desde la base de datos
        if username == 'usuario' and password == 'usuario1234':
            return redirect(url_for('home'))
        else:
            error = 'Credenciales incorrectas. Inténtalo de nuevo.'
    return render_template('login.html', error=error)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('login'))

# Ruta para registrar hospitales
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        conn = get_db_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO Hospital (nombre, direccion, telefono) VALUES (%s, %s, %s)", 
                          (nombre, direccion, telefono))
                conn.commit()
                print("Hospital registrado correctamente")
            except psycopg2.DatabaseError as e:
                print(f"Error al registrar hospital: {e}")
            finally:
                close_db_connection(conn)
        
        return redirect(url_for('home'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

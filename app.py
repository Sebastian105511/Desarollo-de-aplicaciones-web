from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Para usar flash messages

# Configuración de conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sebas1234',
    'database': 'desarrollo_web'
}


# Función para conectar a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


# Ruta principal (Home)
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para el formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validar el usuario en la base de datos
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')


# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Guardar el usuario en la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, password))
        connection.commit()
        connection.close()

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Ruta para listar productos
@app.route('/productos')
def productos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    connection.close()
    return render_template('productos.html', productos=productos)


@app.route('/crear', methods=['GET', 'POST'], endpoint='crear')
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        # Aquí iría la lógica para guardar en la base de datos
        flash('Producto creado con éxito', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'], endpoint='editar')
def editar_producto(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        query = "UPDATE productos SET nombre = %s, precio = %s, stock = %s WHERE id_producto = %s"
        cursor.execute(query, (nombre, precio, stock, id))
        connection.commit()
        connection.close()
        flash('Producto actualizado con éxito', 'success')
        return redirect(url_for('productos'))

    query = "SELECT * FROM productos WHERE id_producto = %s"
    cursor.execute(query, (id,))
    producto = cursor.fetchone()
    connection.close()
    return render_template('formulario.html', producto=producto)


# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_producto(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM productos WHERE id_producto = %s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('productos'))


# Ruta para listar usuarios
@app.route('/usuarios')
def usuarios():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    connection.close()
    return render_template('usuarios.html', usuarios=usuarios)


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)

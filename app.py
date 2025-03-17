from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from Conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'


# Definimos el formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    mail = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')


# Ruta de la página de inicio
@app.route('/')
def index():
    return render_template('index.html')


# Ruta del formulario para agregar usuarios
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        nombre = form.nombre.data
        mail = form.mail.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail) VALUES (%s, %s)", (nombre, mail))
        conexion.commit()
        conexion.close()

        return redirect(url_for('usuarios'))
    return render_template('formulario.html', form=form)


# Ruta para mostrar la lista de usuarios
@app.route('/usuarios')
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()

    return render_template('usuarios.html', usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)

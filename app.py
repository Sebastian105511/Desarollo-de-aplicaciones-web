from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta'

# Definimos el formulario
class MiFormulario(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Enviar')

# Ruta de la página de inicio
@app.route('/index')
def index():
    return render_template('index.html')

# Ruta de la página 'about'
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para mostrar y procesar el formulario
@app.route('/', methods=['GET', 'POST'])
def formulario():
    form = MiFormulario()
    if form.validate_on_submit():
        return render_template('resultado.html', nombre=form.nombre.data)
    return render_template('formulario.html', form=form)

# Ruta para mostrar el resultado después de enviar el formulario
@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
    return render_template('resultado.html')

if __name__ == "__main__":
    app.run(debug=True)

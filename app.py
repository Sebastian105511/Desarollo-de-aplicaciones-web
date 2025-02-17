from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '¡Hola, esta es mi primera aplicación Flask!'

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {Any}!'

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Usa el puerto 5001

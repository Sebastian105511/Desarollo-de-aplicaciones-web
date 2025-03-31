import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sebas1234",
        database="desarrollo_web"
    )

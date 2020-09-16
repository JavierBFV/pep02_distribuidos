from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'clave1235'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Explicaciones de lo que entiendo en el codigo:

#@app.route: Creo que esto hace que se use la funcion, cuando la pagina llega al la ruta escrita en el
#           string entre parentesis
#render_template: Cuando la funcion se inicia, render va a la carpeta de templates y muestra en la
#                aplicacion el archivo que tenga el nombre escrito.

#Funcion Main
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api", methods=['GET'])
def api():
    return{
        'userId': 1,
        'title': 'Flask React Application',
        'completed': False
    }

#Funcion para ingresar un "usuario"
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():
    try:
        # read the posted values from the UI
        _rut = request.form['inputRut']
        _name = request.form['inputName']
        _direccion = request.form['inputDireccion']
        _motivo = request.form['inputMotivo']
        _fecha = request.form['inputFecha']
        _tiempo = request.form['inputTiempo']

        # validate the received values
        if _rut and _name and _direccion and _motivo and _fecha and _tiempo:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_rut, _name, _direccion, _motivo, _fecha, _tiempo))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
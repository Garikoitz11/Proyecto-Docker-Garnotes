import os
import time

from crate import client
from flask import Flask, render_template, request, redirect, session
import ldap
from datetime import datetime, timedelta


app = Flask(__name__, template_folder='templates')

secret_key = os.urandom(24)
app.secret_key = secret_key

connection = client.connect("crate:4200")
cursor = connection.cursor()
   
LDAP_HOST = 'ldap'
LDAP_PORT = 389
LDAP_BASE_DN = 'dc=garnotes,dc=com'
LDAP_ADMIN_USERNAME = 'admin'
LDAP_ADMIN_PASSWORD = 'admin'

notas = []

@app.route('/')
def inicio():
    if 'username' in session:
        return redirect('/notes')
    else:
        return redirect('/login')



@app.route('/login', methods=['GET'])
def loginGet():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def loginPost():
    try:
        username = request.form['username']
        password = request.form['password']

        conn = ldap.initialize(f'ldap://{LDAP_HOST}:{LDAP_PORT}')
        dn = f'cn={username},ou=usuarios,{LDAP_BASE_DN}'
        conn.simple_bind_s(dn, password)

        session['username'] = username
        
        return redirect('/notes')

    except ldap.INVALID_CREDENTIALS:
        return render_template('login.html', error='Usuario o contraseña incorrectos')

    except ldap.LDAPError as e:
        print(f'Error: {e}')

    finally:
        conn.unbind()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
         
        try:
            conn = ldap.initialize(f'ldap://{LDAP_HOST}:{LDAP_PORT}')
            conn.simple_bind_s(f'cn={LDAP_ADMIN_USERNAME},{LDAP_BASE_DN}', LDAP_ADMIN_PASSWORD)

            dn = f'cn={username},ou=usuarios,{LDAP_BASE_DN}'

            attrs = [
                ('objectClass', [b'top', b'person']),
                ('cn', [username.encode('utf-8')]),
                ('sn', [b'TuApellido']),
                ('userPassword', [password.encode('utf-8')]),
            ]

            conn.add_s(dn, attrs)

            conn.unbind()

        except ldap.LDAPError as e:
            print(f'Error al registrar el usuario: {e}')
        
        return redirect('/')

    return render_template('register.html')



@app.route('/notes', methods=['GET'])
def mostrarNotas():
    if 'username' not in session:
        return redirect('/login')

    else:
        idUsuario = session['username']
        
        if idUsuario == 'administrador':
            esAdmin = True
        else:
            esAdmin = False

        if not notas:
            cursor.execute("CREATE TABLE IF NOT EXISTS notas (id text, texto text, fecha TIMESTAMP WITHOUT TIME ZONE);")

            if esAdmin:
                cursor.execute("SELECT * FROM notas ORDER BY fecha ASC")

                notasObtenidas = cursor.fetchall()

                for nota in notasObtenidas:
                    usuario = nota[0]
                    texto = nota[1]
                    fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nota[2] / 1000))
                    notas.append((usuario, texto, fecha))

            else:
                cursor.execute("SELECT * FROM notas WHERE id = ? ORDER BY fecha ASC", (idUsuario,))
        
                notasObtenidas = cursor.fetchall()
    
                for nota in notasObtenidas:
                    texto = nota[1]
                    fecha = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(nota[2] / 1000))
                    notas.append((texto, fecha))
        
        return render_template('notes.html', notas=notas, esAdmin=esAdmin)



@app.route('/notes', methods=['POST'])
def guardarNota():
    idUsuario = session['username']
    texto = request.form['texto']

    cursor.execute("CREATE TABLE IF NOT EXISTS notas (id text, texto text, fecha TIMESTAMP WITHOUT TIME ZONE);")

    timenow = datetime.now()

    cursor.execute("INSERT INTO notas (id, texto, fecha) VALUES (?, ?, ?)", (idUsuario,texto,timenow))

    notas.append((texto, timenow.strftime("%Y-%m-%d %H:%M:%S")))

    return redirect('/notes')



@app.route('/logout', methods=['POST'])
def cerrarSesion():
    session.clear()
    notas.clear()

    return redirect('/login')

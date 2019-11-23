
from io import StringIO

from flask import Flask, redirect, url_for
from flask import render_template
from flask_mysqldb import MySQL
from flask import request
from flask import make_response
from reportlab.pdfgen import canvas
import pdfkit
import os
from fpdf import FPDF

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='msc2019'
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'templates/'
mysql=MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM empelado")
    data=cur.fetchall()
    cur.close()
    return render_template('Empleado.html',empleado=data)

@app.route('/insertar',methods=["POST"])
def insertar():
    if request.method == 'POST':
        claves = request.form['clave']
        nombres= request.form['nombre']
        sueldos= request.form['sueldo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empelado (clave,nombre,sueldo) VALUES (%s,%s,%s)",(claves,nombres,sueldos))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))

@app.route('/editar', methods=["POST"])
def editar():
    if request.method == 'POST':
        claves = request.form['clave']
        nombres= request.form['nombre']
        sueldos= request.form['sueldo']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE empelado SET nombre=%s,sueldo=%s WHERE clave=%s", (nombres,sueldos,claves))
        mysql.connection.commit()
        return redirect(url_for('home'))
    else:
        return "ok"

@app.route('/eliminar/<string:id>', methods=["GET"])
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM empelado WHERE clave=%s", (id))
    mysql.connection.commit()
    return redirect(url_for('home'))


@app.route("/pdf")
def pdf(spacing=1):
    '''data = [['First Name', 'Last Name', 'email', 'zip'],
            ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
            ['John', 'Doe', 'jdoe@doe.com', '12345'],
            ['Nina', 'Ma', 'inane@where.com', '54321']
            ]'''

    # print(data)
    # Cadena SQL para recuperar los datos del servidor
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM empelado"

    # Ejectuamos la cadena sql
    cur.execute(sql)

    # Se almacena la respuesta del servidor
    result = cur.fetchall()

    data = [['Clave', 'Nombre', 'Sueldo']]
    for row in result:
        lista = [str(row[0]), row[1], str(row[2])]
        data.append(lista)
    # print(data)

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 3.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * spacing,
                     txt=item, border=1)
        pdf.ln(row_height * spacing)

    pdf.output('Reporte1.pdf')

    return render_template("Empleado.html",empleado=result)

if __name__ == '__main__':
    app.run(debug=True)


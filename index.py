from flask import Flask, render_template, request, redirect, flash
import controlador_signos

from flask import Response

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#matplotlib.use('TkAgg')
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import random
from flask import Response

import os
from bd import obtener_conexion

import logging

import pymysql
from os import remove

from flask import url_for

app = Flask(__name__)

    #data = pd.read_csv('C:\\Users\\sandr\\?.csv')
    #x = variables['?']

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/agregar_signo")
def formulario_agregar_signo():
    return render_template("agregar_signo.html")

#Función para enviar datos un registro a la base de datos
@app.route("/guardar_signo", methods=["POST"])
def guardar_signo():
    signo_zodiacal = request.form["signo_zodiacal"]
    p1 = request.form["p1"]
    p2 = request.form["p2"]
    p3 = request.form["p3"]
    p4 = request.form["p4"]
    p5 = request.form["p5"]
    p6 = request.form["p6"]
    p7 = request.form["p7"]
    p8 = request.form["p8"]
    p9 = request.form["p9"]
    p10 = request.form["p10"]
    p11 = request.form["p11"]
    p12 = request.form["p12"]
    p13 = request.form["p13"]
    p14 = request.form["p14"]
    p15 = request.form["p15"]
    p16 = request.form["p16"]

    controlador_signos.insertar_signo(signo_zodiacal, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16)
    
    #Vuelve a generar el csv para que tenga el nuevo registro
    conn = pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')
    sql_query = pd.read_sql_query('SELECT * FROM signos_zodiacales'
                                ,conn)
    df = pd.DataFrame(sql_query)
    remove(r'static\data\exported_data.csv')
    remove(r'static\data\exported_data.xlsx')
    df.to_csv(r'static\data\exported_data.csv', index = False) 
    df.to_excel(r'static\data\exported_data.xlsx', index=False)
    
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/signos")

@app.route("/signos")
def signos():
    registros = controlador_signos.obtener_registros()

    #Vuelve a generar el csv para que este actualizado con la BD
    conn = pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')
    sql_query = pd.read_sql_query('SELECT * FROM signos_zodiacales'
                                ,conn)
    df = pd.DataFrame(sql_query)
    remove(r'static\data\exported_data.csv')
    remove(r'static\data\exported_data.xlsx')
    df.to_csv(r'static\data\exported_data.csv', index = False) 
    df.to_excel(r'static\data\exported_data.xlsx', index=False)

    return render_template("signos.html", registros=registros)


'''
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

@app.route('/clusters')
def clusters():
  lnx=np.log(x)
  plt.plot(lnx)   
  plt.savefig('./static/img/new_plot.png')
  return render_template('clusters.html', name = 'new_plot', url ='./static/img/new_plot.png')
'''

@app.route('/cluster')
def cluster():
    plt.switch_backend('agg')
    controlador_signos.analisisClusters()
    plt.close()
    return redirect("/clusters")
    

@app.route('/clusters')
def clusters():
    controlador_signos.mostrarCentroides()
    plt.close()
    pred = request.args.get('prediccion', None)
    registros = controlador_signos.obtener_registros()
    return render_template('clusters.html', name = 'Codo', url_codo ='./static/img/codo.png', url_centroides = './static/img/centroides.png', prediccion = pred, registros = registros)


#Función para método que genera la gráfica de estadistica seleccionada
@app.route('/graficaEstadisticas', methods=["POST"])
def graficaEstadisticas():
    slcCaracteristicas = request.form["slcCaracteristicas"]
    print(slcCaracteristicas)
    plt.switch_backend('agg')
    controlador_signos.graficaEstadisticas(str(slcCaracteristicas))
    controlador_signos.graficaSignos()
    plt.close() # Cierra los gráficos de plt para que no tengan conflicto entre ellos al volver a ejecutar graficaSignos()
    return redirect("/estadisticas")
    

#Función para ruta de pantalla de estadisticas
@app.route('/estadisticas')
def estadisticas():
    controlador_signos.graficaSignos()
    return render_template('estadisticas.html', name = 'Estadísticas de los datos', url_signos = './static/img/grafica_cantidad_signos.png', url_caracteristicas ='./static/img/grafica_cantidad.png')


@app.route("/entrenar", methods=["POST"])
def entrenarAlgoritmo():
    nclusters = request.form["nclusters"]
    controlador_signos.entrenar_algoritmo(nclusters)
    return redirect("/clusters")


#Función para predecir signo
@app.route('/predecirSigno', methods=["POST"])
def predecirSigno():
    nMuestra = request.form["nMuestra"]
    res = controlador_signos.predecirSigno(int(nMuestra))
    return redirect(url_for("clusters", prediccion=res))


@app.route('/', methods = ['GET', 'POST']) 
def index(): 
    if request.method == 'POST': 
        date = request.form.get('date') 
        return redirect(url_for('booking', date=date)) 
    return render_template('main/index.html') 
    
@app.route('/booking') 
def booking(): 
    date = request.args.get('date', None) 
    return render_template('main/booking.html', date=date)


if __name__ == '__main__':
    app.run(debug=True)

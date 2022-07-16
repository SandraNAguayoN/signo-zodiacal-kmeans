from flask import Flask, render_template, request, redirect, flash
import controlador_signos

from flask import Response

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import os
from bd import obtener_conexion



app = Flask(__name__)

variables = pd.read_csv('C:\\Users\\sandr\\exported_data.csv')
x =variables['signo_zodiacal']


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/agregar_signo")
def formulario_agregar_signo():
    return render_template("agregar_signo.html")


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
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/signos")

@app.route("/signos")
def signos():
    registros = controlador_signos.obtener_registros()
    return render_template("signos.html", registros=registros)


'''@app.route('/clusters')
def clusters():
    lnx=np.log(x)
    plt.plot(lnx)
    return render_template('clusters.html', name = plt.show())'''

'''@app.route('/clusters')
def clusters():
    return render_template('clusters.html')'''

@app.route('/clusters')
def clusters():
  lnx=np.log(x)
  plt.plot(lnx)   
  plt.savefig('./static/img/new_plot.png')
  return render_template('clusters.html', name = 'new_plot', url ='./static/img/new_plot.png')


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



if __name__ == '__main__':
    app.run(debug=True)

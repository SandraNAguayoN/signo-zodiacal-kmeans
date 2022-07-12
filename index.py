from flask import Flask, render_template, request, redirect, flash
import controlador_signos

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/clusters')
def clusters():
    return render_template('clusters.html')


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

if __name__ == '__main__':
    app.run(debug=True)

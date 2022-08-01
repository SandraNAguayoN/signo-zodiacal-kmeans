from bd import obtener_conexion

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans

#Función para crear un registro a la base de datos
def insertar_signo(signo_zodiacal, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO signos_zodiacales(signo_zodiacal, lider, cri_exi, ama_car, decidido, afe_sen, extrovertido, sociable, analitico, trabajo_equipo, compulsiva, conf_lea, opt_ale, ene_cur, tran_seg, senc_pac, organizado) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)",
                       (str(signo_zodiacal), str(p1), str(p2), str(p3), str(p4), str(p5), str(p6), str(p7), str(p8), str(p9), str(p10), str(p11), str(p12), str(p13), str(p14), str(p15), str(p16)))
    conexion.commit()
    conexion.close()


def obtener_registros():
    conexion = obtener_conexion()
    registros = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, signo_zodiacal, lider, cri_exi, ama_car, decidido, afe_sen, extrovertido, sociable, analitico, trabajo_equipo, compulsiva, conf_lea, opt_ale, ene_cur, tran_seg, senc_pac, organizado FROM signos_zodiacales")
        registros = cursor.fetchall()
    conexion.close()
    return registros

"""
def eliminar_dato(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM juegos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_juego_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precio FROM juegos WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego


def actualizar_juego(nombre, descripcion, precio, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE juegos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
                       (nombre, descripcion, precio, id))
    conexion.commit()
    conexion.close()

"""

def analisisClusters():
    data = pd.read_csv('C:\\Users\\sandr\\exported_data.csv')
    data = data.drop(['id'], axis = 1)

    #Se selecionan unos datos al azar para posteriormente verificar el clúster al que pertenecen
    indices = [23, 24, 25]
    muestras = pd.DataFrame(data.loc[indices], 
                        columns = data.keys()).reset_index(drop = True)
    data = data.drop(indices, axis = 0)

    #Eliminamos las columnas de región y canal 
    data = data.drop(['signo_zodiacal'], axis = 1)
    muestras = muestras.drop(['signo_zodiacal'], axis = 1)

    #Se realiza el escalamiento de los datos
    data_escalada = preprocessing.Normalizer().fit_transform(data)
    muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)
    
    ### ANÁLISIS DE MACHINE LEARNING ###
    #Se determina las variables a evaluar
    X = data_escalada.copy()

    ## Hallar el valor óptimo de K ##
    #Se aplicará el método de codo para hallar K
    #Se calcula el algoritmo de agrupación para diferentes valores de K
    inercia = [] 
    for i in range(1, 20):
        algoritmo = KMeans(n_clusters = i, init = 'k-means++', 
                        max_iter = 300, n_init = 10)
        algoritmo.fit(X)
        #Para cada K, se calcula la suma total del cuadrado dentro del clúster
        inercia.append(algoritmo.inertia_)

    #Se traza la curva de la suma de errores cuadráticos 
    plt.figure(figsize=[5,6])
    plt.title('Método del Codo')
    plt.xlabel('No. de clusters')
    plt.ylabel('Inercia')
    return plt.plot(list(range(1, 20)), inercia, marker='o')
    #return plt.show()

def entrenarAlgoritmo(nclusters):
    data = pd.read_csv('C:\\Users\\sandr\\signos_zodiacales_2.csv')

    #Se selecionan unos datos al azar para posteriormente verificar el clúster al que pertenecen
    indices = [23, 24, 25]
    muestras = pd.DataFrame(data.loc[indices], 
                        columns = data.keys()).reset_index(drop = True)
    data = data.drop(indices, axis = 0)

    #Eliminamos las columnas de región y canal 
    data = data.drop(['signo_zodiacal'], axis = 1)
    muestras = muestras.drop(['signo_zodiacal'], axis = 1)

    #Se realiza el escalamiento de los datos
    data_escalada = preprocessing.Normalizer().fit_transform(data)
    muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)
    
    ### ANÁLISIS DE MACHINE LEARNING ###
    #Se determina las variables a evaluar
    X = data_escalada.copy()

    ## Se aplica el algoritmo de clustering ##
    #Se define el algoritmo junto con el valor de K
    algoritmo = KMeans(n_clusters = int(nclusters), init = 'k-means++',  #se pasa el n de clusters que se especificó en el form
                    max_iter = 300, n_init = 10)
    #Se entrena el algoritmo
    algoritmo.fit(X)


def predecir_signo(nClusters):
    #obtener el ultimo registro de la bd
    data = pd.read_csv('C:\\Users\\sandr\\signos_zodiacales_2.csv')

    #Se selecionan unos datos al azar para posteriormente verificar el clúster al que pertenecen
    indices = [23, 24, 25]
    muestras = pd.DataFrame(data.loc[indices], 
                        columns = data.keys()).reset_index(drop = True)
    data = data.drop(indices, axis = 0)

    #Eliminamos las columnas de región y canal 
    data = data.drop(['signo_zodiacal'], axis = 1)
    muestras = muestras.drop(['signo_zodiacal'], axis = 1)

    #Se realiza el escalamiento de los datos
    data_escalada = preprocessing.Normalizer().fit_transform(data)
    muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)
    
    ### ANÁLISIS DE MACHINE LEARNING ###
    #Se determina las variables a evaluar
    X = data_escalada.copy()

    ## Se aplica el algoritmo de clustering ##
    #Se define el algoritmo junto con el valor de K
    algoritmo = KMeans(n_clusters = int(nclusters), init = 'k-means++',  #se pasa el n de clusters que se especificó en el form
                    max_iter = 300, n_init = 10)
    #Se entrena el algoritmo
    algoritmo.fit(X)

def graficaSignos():
    data = pd.read_csv(r'static\data\exported_data.csv')
    data = data.drop(['id'], axis = 1)
    signos = data['signo_zodiacal']
    mapa_signos = {}

    for signo in signos:
        if signo in mapa_signos:
            mapa_signos[signo] += 1
        else:
            mapa_signos[signo] = 1

    for valor in sorted(mapa_signos):
        print(f'{valor}: {mapa_signos[valor]}')
        
    intervalos = range(min(signos), max(signos) + 1) #calculamos los extremos de los intervalos

    plt.hist(x=signos, bins=intervalos, color='#F6BC8C', rwidth=0.85)
    plt.title('Cantidad de personas por signo zodiacal')
    plt.xlabel('Signo zodiacal')
    plt.ylabel('Cantidad de personas')
    plt.xticks(intervalos)
  
    plt.savefig('./static/pdf/grafica_cantidad_signos.pdf')   # Guardar en formato .pdf
    return plt.savefig('./static/img/grafica_cantidad_signos.png') # Guardar en formato .png

def graficaEstadisticas(slcCaracteristicas):
    data = pd.read_csv(r'static\data\exported_data.csv')
    data = data.drop(['id'], axis = 1)
    caracteristicas = data[slcCaracteristicas]
    valores = ['No', 'Si']

    mapa_caracteristicas = {}

    for caracteristica in caracteristicas:
        if caracteristica in mapa_caracteristicas:
            mapa_caracteristicas[caracteristica] += 1
        else:
            mapa_caracteristicas[caracteristica] = 1

    for valor in sorted(mapa_caracteristicas):
        print(f'{valor}: {mapa_caracteristicas[valor]}')

    res = data.groupby([slcCaracteristicas]).agg({
    slcCaracteristicas: 'count'
    })
    print(res)
    no = res[slcCaracteristicas].values[0]
    si = res[slcCaracteristicas].values[1]

    columna = slcCaracteristicas
    titulo = ''

    if str(columna) == 'lider':
        titulo = 'Cantidad de personas que son "Líderes"'
    elif columna == 'cri_exi':
        titulo = 'Cantidad de personas que son "Críticas y exigentes"'
    elif columna == 'ama_car':
        titulo = 'Cantidad de personas que son "Amables y cariñosas"'
    elif columna == 'decidido':
        titulo = 'Cantidad de personas que son "Decididas"'
    elif columna == 'afe_sen':
        titulo = 'Cantidad de personas que son "Afectuosas y sentimentales"'
    elif columna == 'extrovertido':
        titulo = 'Cantidad de personas que son "Extrovertidas"'
    elif columna == 'sociable':
        titulo = 'Cantidad de personas que son "Sociables"'
    elif columna == 'analitico':
        titulo = 'Cantidad de personas que son "Analíticas"'
    elif columna == 'trabajo_equipo':
        titulo = 'Cantidad de personas que les gusta el "Trabajo en equipo"'
    elif columna == 'compulsiva':
        titulo = 'Cantidad de personas que son "Compulsivas"'
    elif columna == 'conf_lea':
        titulo = 'Cantidad de personas que son "Confiables y leales"'
    elif columna == 'opt_ale':
        titulo = 'Cantidad de personas que son "Optimistas y alegres"'
    elif columna == 'ene_cur':
        titulo = 'Cantidad de personas que son "Enérgicas y curiosas"'
    elif columna == 'tran_seg':
        titulo = 'Cantidad de personas que son "Tranquilas y seguras"'
    elif columna == 'senc_pac':
        titulo = 'Cantidad de personas que son "Sencillas y pacíficas"'
    elif columna == 'organizado':
        titulo = 'Cantidad de personas que son "Organizadas"'
    else:
        titulo = 'Error: No se pudo obtener el título'

    plt.title(titulo)

    plt.pie(x=res[slcCaracteristicas], labels=valores, autopct="%0.1f %%")

    plt.savefig('./static/pdf/grafica_cantidad.pdf') # Guardar en formato .pdf
    return plt.savefig('./static/img/grafica_cantidad.png') # Guardar en formato .png


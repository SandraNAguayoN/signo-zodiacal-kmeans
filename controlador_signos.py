from bd import obtener_conexion

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.cluster import KMeans

import csv

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
    data = pd.read_csv(r'static\data\exported_data.csv')
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
    plt.figure(figsize=[4,4])
    plt.title('Método del Codo')
    plt.xlabel('No. de clusters')
    plt.ylabel('Inercia')
    plt.plot(list(range(1, 20)), inercia, marker='o')
    return plt.savefig('./static/img/codo.png')
    #return plt.show()


def mostrarCentroides():
    #### CARGAR LOS DATOS ####
    data = pd.read_csv(r'static\data\exported_data.csv')
    data = data.drop(['id'], axis = 1)

    ### DATOS DE MUESTRA ###
    #Se selecionan unos datos al azar para posteriormente verificar el clúster 
    #al que pertenecen
    indices = [23, 24, 25]
    #indices = [23]
    muestras = pd.DataFrame(data.loc[indices], 
                        columns = data.keys()).reset_index(drop = True)
    data = data.drop(indices, axis = 0)

    ### PROCESAMIENTO DE LOS DATOS ###
    #Eliminamos las columnas 
    data = data.drop(['signo_zodiacal'], axis = 1)
    muestras = muestras.drop(['signo_zodiacal'], axis = 1)

    #Se realiza el escalamiento de los datos
    from sklearn import preprocessing

    data_escalada = preprocessing.Normalizer().fit_transform(data)
    muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)

    ### ANÁLISIS DE MACHINE LEARNING ###
    from sklearn.cluster import KMeans

    #Se determina las variables a evaluar
    X = data_escalada.copy()

    ## Se aplica el algoritmo de clustering ##
    #Se define el algoritmo junto con el valor de K
    algoritmo = KMeans(n_clusters = 12, init = 'k-means++', 
                    max_iter = 300, n_init = 10)

    #Se entrena el algoritmo
    algoritmo.fit(X)

    #Se obtiene los datos de los centroides y las etiquetas
    centroides, etiquetas = algoritmo.cluster_centers_, algoritmo.labels_

    ### GRAFICAR LOS DATOS JUNTO A LOS RESULTADOS ###
    # Se aplica la reducción de dimensionalidad a los datos
    from sklearn.decomposition import PCA

    modelo_pca = PCA(n_components = 2)
    modelo_pca.fit(X)
    pca = modelo_pca.transform(X) 

    #Se aplica la reducción de dimsensionalidad a los centroides
    centroides_pca = modelo_pca.transform(centroides)

    # Se define los colores de cada clúster
    colores = ['blue', 'red', 'green', 'orange', 'gray', 'brown', 'pink', 'yellow', '#C8820F', '#0FC8C2', '#B96363', '#47FF2E']

    #Se asignan los colores a cada clústeres
    colores_cluster = [colores[etiquetas[i]] for i in range(len(pca))]

    #Se grafica los componentes PCA
    plt.scatter(pca[:, 0], pca[:, 1], c = colores_cluster, 
                marker = 'o',alpha = 0.4)

    #Se grafican los centroides
    plt.scatter(centroides_pca[:, 0], centroides_pca[:, 1],
                marker = 'x', s = 100, linewidths = 3, c = colores)

    #Se guadan los datos en una variable para que sea fácil escribir el código
    xvector = modelo_pca.components_[0] * max(pca[:,0])
    yvector = modelo_pca.components_[1] * max(pca[:,1])
    columnas = data.columns

    #Se grafican los nombres de los clústeres con la distancia del vector
    for i in range(len(columnas)):
        #Se grafican los vectores
        plt.arrow(0, 0, xvector[i], yvector[i], color = 'black', 
                width = 0.0005, head_width = 0.02, alpha = 0.75)
        #Se colocan los nombres
        plt.text(xvector[i], yvector[i], list(columnas)[i], color='black', 
                alpha=0.75)

    return plt.savefig('./static/img/centroides.png')


def predecirSigno(nMuestra):
    #### CARGAR LOS DATOS ####
    data = pd.read_csv(r'static\data\exported_data.csv')
    data = data.drop(['id'], axis = 1)

    ### DATOS DE MUESTRA ###
    #Se selecionan unos datos al azar para posteriormente verificar el clúster 
    #al que pertenecen
    #indices = [23, 24, 25]
    indices = [nMuestra-1]
    muestras = pd.DataFrame(data.loc[indices], 
                        columns = data.keys()).reset_index(drop = True)
    data = data.drop(indices, axis = 0)

    ### PROCESAMIENTO DE LOS DATOS ###
    #Eliminamos las columnas 
    data = data.drop(['signo_zodiacal'], axis = 1)
    muestras = muestras.drop(['signo_zodiacal'], axis = 1)

    #Se realiza el escalamiento de los datos
    from sklearn import preprocessing

    data_escalada = preprocessing.Normalizer().fit_transform(data)
    muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)

    ### ANÁLISIS DE MACHINE LEARNING ###
    from sklearn.cluster import KMeans

    #Se determina las variables a evaluar
    X = data_escalada.copy()

    ## Se aplica el algoritmo de clustering ##
    #Se define el algoritmo junto con el valor de K
    algoritmo = KMeans(n_clusters = 12, init = 'k-means++', 
                    max_iter = 300, n_init = 10)

    #Se entrena el algoritmo
    algoritmo.fit(X)

    #Se obtiene los datos de los centroides y las etiquetas
    centroides, etiquetas = algoritmo.cluster_centers_, algoritmo.labels_

    #Utilicemos los datos de muestras y verifiquemos en que cluster se encuentran
    muestra_prediccion = algoritmo.predict(muestras_escalada)

    for i, pred in enumerate(muestra_prediccion):
        print("Muestra", i, "se encuentra en el clúster:", pred)
        prediccion = pred
        
    if prediccion == 0:
        pred = 'Capricornio'
    elif prediccion == 1:
        pred = 'Acuario'
    elif prediccion == 2:
        pred = 'Piscis'
    elif prediccion == 3:
        pred = 'Aries'
    elif prediccion == 4:
        pred = 'Tauro'
    elif prediccion == 5:
        pred = 'Géminis'
    elif prediccion == 6:
        pred = 'Cáncer'
    elif prediccion == 7:
        pred = 'Leo'
    elif prediccion == 8:
        pred = 'Virgo'
    elif prediccion == 9:
        pred = 'Libra'
    elif prediccion == 10:
        pred = 'Escorpio'
    elif prediccion == 11:
        pred = 'Sagitario'

    return f'{nMuestra} es {pred}'

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

def cargarDataBaseDatos(sRuta):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        with open(sRuta, 'r') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            for row in reader:
                if row[0] != 'signo_zodiacal': #No toma en cuenta la primera fila que contiene los nombres de las columnas
                    cursor.execute(
                    "INSERT INTO signos_zodiacales (signo_zodiacal, lider, cri_exi, ama_car, decidido, afe_sen, extrovertido, sociable, analitico, trabajo_equipo, compulsiva, conf_lea, opt_ale, ene_cur, tran_seg, senc_pac, organizado) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)",
                    (str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]), str(row[11]), str(row[12]), str(row[13]), str(row[14]), str(row[15]), str(row[16]))
                    )
            csvFile.close()
    conexion.commit()
    conexion.close()

def cantidadTotalRegistros():
    conexion = obtener_conexion()
    cantidad = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM signos_zodiacales")
        cantidad = cursor.fetchone()
        
    print("Esta es la cantidad",cantidad)
    conexion.close()
    return cantidad
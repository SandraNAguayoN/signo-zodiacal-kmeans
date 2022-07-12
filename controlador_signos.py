from bd import obtener_conexion


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
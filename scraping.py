import requests
from bs4 import BeautifulSoup
from dbhelper import DBHelper
import sys


db = DBHelper()

def eliminarAcentos(cadena):

    d = {    '\xc1':'A',
        '\xc9':'E',
        '\xcd':'I',
        '\xd3':'O',
        '\xda':'U',
        '\xdc':'U',
        '\xd1':'N',
        '\xc7':'C',
        '\xed':'i',
        '\xf3':'o',
        '\xf1':'n',
        '\xe7':'c',
        '\xba':'',
        '\xb0':'',
        '\x3a':'',
        '\xe1':'a',
        '\xe2':'a',
        '\xe3':'a',
        '\xe4':'a',
        '\xe5':'a',
        '\xe8':'e',
        '\xe9':'e',
        '\xea':'e',
        '\xeb':'e',
        '\xec':'i',
        '\xed':'i',
        '\xee':'i',
        '\xef':'i',
        '\xf2':'o',
        '\xf3':'o',
        '\xf4':'o',
        '\xf5':'o',
        '\xf0':'o',
        '\xf9':'u',
        '\xfa':'u',
        '\xfb':'u',
        '\xfc':'u',
        '\xe5':'a'
}

    nueva_cadena = cadena
    for c in d.keys():
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    return nueva_cadena

def web_scraping(id_facultad, nombre_facultad):

    # comenzamos a hacer scraping

    url = "https://www.unl.edu.ar/agenda/bedelia/index.php?id_facultad=" + id_facultad + "&KeepThis=true&TB_iframe=true&height=500&width=650"

    pagina = requests.get(url,timeout=5)

    soup = BeautifulSoup(pagina.content, "html.parser")

    hora = soup.find(class_="hora")

    if (hora):
        hora.decompose()
    horarios = soup.find_all(class_="hora")
    array_horarios=[]

    for hora in horarios:
        hora = hora.text.encode('utf-8').decode('ascii', 'ignore')
        array_horarios.append(hora)

    materia = soup.find(class_="materia")

    if (materia):
        materia.decompose()
    materias = soup.find_all(class_="materia")
    array_materias=[]

    for materia in materias:
        #materia = materia.text.encode('utf8').decode('ascii', 'ignore')
        materia = eliminarAcentos(materia.text)
        array_materias.append(materia)

    comision = soup.find(class_="comision")

    if (comision):
        comision.decompose()
    comisiones = soup.find_all(class_="comision")
    array_comisiones=[]

    for comision in comisiones:
        #comision = comision.text.encode('utf-8').decode('ascii', 'ignore')
        comision = eliminarAcentos(comision.text)
        array_comisiones.append(comision)

    aula = soup.find(class_="aula")

    if (aula):
        aula.decompose()
    aulas = soup.find_all(class_="aula")
    array_aulas=[]


    for aula in aulas:
        #aula = aula.text.encode('utf-8').decode('ascii', 'ignore')
        aula = eliminarAcentos(aula.text)
        array_aulas.append(aula)

    bedelia_size = len(array_materias)

    if (bedelia_size == 0): # si no hay materias en bedelia
        db.vaciar_tabla(nombre_facultad)
        # print("entro en 1")
    else:
        print("Hay materias en bedelia")
        lista = db.get_contenido_tabla(nombre_facultad).fetchall()
        table_size = len(lista)
        if(table_size == 0): # si hay materias en bedelia pero no hay materias en la BBDD
            # print("No hay materias en la BBDD")
            i = 0
            while(i<bedelia_size):
                db.agregar_materia(nombre_facultad, array_horarios[i], array_materias[i], array_comisiones[i], array_aulas[i])
                i = i+1
        else:
            # si hay materias en bedelia y tambien en la base
            lista = db.get_contenido_tabla(nombre_facultad).fetchall()
            # print("Hay materias en la BBDD")
            materia_en_bbdd = False
            i = 0
            j = 0
            # comprobar que si no existe una materia de bedelia en la BBDD, agregarla a la BBDD
            while(i<bedelia_size):
                while(j<table_size):
                    if(array_horarios[i] == lista[j][1] and array_materias[i] == lista[j][2] and array_comisiones[i] == lista[j][3] and array_aulas[i] == lista[j][4]):
                        materia_en_bbdd = True
                        # print("La materia ya esta en la BBDD")
                        break
                    j += 1

                if(materia_en_bbdd == False):
                    db.agregar_materia(nombre_facultad, array_horarios[i], array_materias[i], array_comisiones[i], array_aulas[i])
                    # print("Se agrego una materia")

                materia_en_bbdd = False
                i += 1
                j = 0

            i = 0
            j = 0

            materia_en_bedelia = False
            # comprobar que si no existe una materia de la BBDD en bedelia, eliminarla de la BBDD
            while(i<table_size):
                while(j<bedelia_size):
                    if(lista[i][1] == array_horarios[j] and lista[i][2] == array_materias[j] and lista[i][3] == array_comisiones[j] and lista[i][4] == array_aulas[j]):
                        materia_en_bedelia = True
                        break
                    j += 1

                if(materia_en_bedelia == False):
                    # print("Se elimino una materia")
                    db.eliminar_materia(nombre_facultad, lista[i][0])

                materia_en_bedelia = False
                j = 0
                i += 1

    #db.vaciar_tabla(nombre_facultad)

web_scraping("14", "fcjs")
web_scraping("16", "fbcb")
web_scraping("18", "fcm")
web_scraping("21", "fich")

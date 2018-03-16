import json
import requests
import time
import urllib
from dbhelper import DBHelper

db = DBHelper()


TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

facultades = ["fich", "fbcb", "fcm", "fcjs", "Volver al menu \U0001f519"]
menu = ["Leeme \U0001f4cb", "Mostrar facultades \U0001f393", "Configuracion \U0001f527",]


def buscar_materia(text, facultad):
    contenido = []
    contenido = db.get_materias(facultad).fetchall()
    materia = []
    j = 0
    for i in range(0, len(contenido)):
        if(i == contenido[j][1]):
            materia.append(i)
        j += 1

    return materia


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def mostrar_materias(nombre_facultad, chat):
    lista = db.get_contenido_tabla(nombre_facultad).fetchall()
    tamanio = len(lista)
    if(tamanio > 0):
        horarios = db.get_horarios(nombre_facultad)
        materias = db.get_materias(nombre_facultad)
        comisiones = db.get_comisiones(nombre_facultad)
        aulas = db.get_aulas(nombre_facultad)

        join = []
        join.append("Volver al menu \U0001f519")
        cadena = ""
        for i in range(0, tamanio):
            cadena = horarios[i] + " | " + materias[i] + " | " + comisiones[i] + " | " + aulas[i]
            join.append(cadena)

        join.append("Volver al menu \U0001f519")
        keyboard = build_keyboard(join)
        send_message("Estas son las materias", chat, keyboard)
    else:
        keyboard = build_keyboard(menu)
        send_message("No hay materias para mostrar", chat, keyboard)

def handle_update(update):
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]

        if text == "/start":
            keyboard = build_keyboard(menu)
            send_message("Bienvenidos :)", chat, keyboard)

        if text == "Leeme \U0001f4cb":
            keyboard = build_keyboard(menu)
            send_message("El fomato con el que se muestra la informacion de cada materia es HORA | MATERIA | COMISION | AULA", chat, keyboard)

        if text == "Mostrar facultades \U0001f393":
            keyboard = build_keyboard(facultades)
            send_message("Mostrando facultades...", chat, keyboard)

        if text == "fcjs":
             mostrar_materias("fcjs", chat)
        if text == "fbcb":
             mostrar_materias("fbcb", chat)
        if text == "fcm":
             mostrar_materias("fcm", chat)
        if text == "fich":
             mostrar_materias("fich", chat)

        if text == "Volver al menu \U0001f519":
            keyboard = build_keyboard(menu)
            send_message("Volviendo al menu principal", chat, keyboard)

        if text == "Configuracion \U0001f527":
            keyboard = build_keyboard(menu)
            send_message("Proximamente...", chat, keyboard)


def handle_updates(updates):
    global ultimo_comando
    for update in updates["result"]:
       handle_update(update)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": False}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

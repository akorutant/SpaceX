import requests
from tkinter import *
from googletrans import Translator
import sqlite3 as sq
from tkinter import ttk

def sort_by(key):
    def wrapper():
        with sq.connect("SpaceX.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM rockets ORDER BY (?)", (key))
            data = cur.fetchall()
            for i in t1.get_children():
                t1.delete(i)
            for row in data:
                t1.insert("", END, values=row)
    return wrapper


URL = "https://api.spacexdata.com/v4/rockets"
translator = Translator()
res = requests.get(URL)
rockets = res.json()
new_rockets = []
for rocket in rockets:
    height = rocket["height"]["meters"]
    diameter = rocket["diameter"]['meters']
    mass = rocket["mass"]["kg"]
    name = rocket["name"]
    wiki = rocket["wikipedia"]
    desc = rocket["description"]
    fuel = rocket["engines"]["propellant_2"]
    desc = translator.translate(desc, dest='ru', src='en').text
    desc = desc.replace("(", "")
    desc = desc.replace(")", "")
    new_rockets.append((name, height, diameter, mass, fuel, desc, wiki))


with sq.connect("SpaceX.db") as con:
    cur = con.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS rockets (
        name TEXT,
        height REAL,
        diam REAL,
        mass REAL,
        fuel TEXT,
        desc TEXT,
        wiki TEXT
        )"""
    )
    cur.execute("SELECT * FROM rockets")
    data = cur.fetchall()

    if data:
        pass
    else:
        for r in new_rockets:
            print(r)
            cur.execute(
                "INSERT INTO rockets(name, height, diam, mass, fuel, desc, wiki)  VALUES (?, ?, ?, ?, ?, ?, ?);",
                (r[i] for i in range(7))
            )
            con.commit()


window = Tk()
window.title("SpaceX")
window.geometry("900x600")

columns = (f'#{i}' for i in range(1, 7))
texts = ('Название', 'Высота', 'Диаметр', 'Масса', 'Тип топлива', 'Описание', 'Википедия')
names = ('name', 'height', 'diam', 'mass', 'fuel', 'desc', 'wiki')
t1 = ttk.Treeview(window, show="headings", columns=columns)

for column, text, command_name in zip(columns, texts, names):
    t1.heading(column, text=text, command=sort_by(command_name))
t1.pack(expand=1, fill=BOTH)
with sq.connect("SpaceX.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM rockets")
    data = cur.fetchall()
    for row in data:
        t1.insert("", END, values=row)


window.mainloop()

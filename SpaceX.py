import requests
from tkinter import *
from googletrans import Translator
import sqlite3 as sq
from tkinter import ttk

def sort_name1():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY name")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name2():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY height")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name3():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY diam")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name4():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY mass")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name5():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY fuel")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name6():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY desc")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)

def sort_name7():
    with sq.connect("SpaceX.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM rockets ORDER BY wiki")
        data = cur.fetchall()
        for i in t1.get_children(): t1.delete(i)
        for row in data:
            t1.insert("", END, values=row)


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

    cur.execute("""CREATE TABLE IF NOT EXISTS rockets (
    name TEXT,
    height REAL,
    diam REAL,
    mass REAL,
    fuel TEXT,
    desc TEXT,
    wiki TEXT
    )""")
    cur.execute("SELECT * FROM rockets")
    data = cur.fetchall()

    if data:
        pass
    else:
        for r in new_rockets:
            print(r)
            cur.execute(
                f"INSERT INTO rockets(name, height, diam, mass, fuel, desc, wiki)  VALUES('{r[0]}',{r[1]},{r[2]},{r[3]},'{r[4]}','{r[5]}','{r[6]}');")
            con.commit()


window = Tk()
window.title("SpaceX")
window.geometry("900x600")

columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
t1 = ttk.Treeview(window, show="headings", columns=columns)
t1.heading("#1", text="Название", command=sort_name1)
t1.heading("#2", text="Высота", command=sort_name2)
t1.heading("#3", text="Диаметр", command=sort_name3)
t1.heading("#4", text="Масса", command=sort_name4)
t1.heading("#5", text="Тип топлива", command=sort_name5)
t1.heading("#6", text="Описание", command=sort_name6)
t1.heading("#7", text="Википедия", command=sort_name7)
t1.pack(expand=1, fill=BOTH)
with sq.connect("SpaceX.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM rockets")
    data = cur.fetchall()
    for row in data:
        t1.insert("", END, values=row)


window.mainloop()

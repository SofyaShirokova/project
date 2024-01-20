import sqlite3

connection = sqlite3.connect('SportZal.sqlite')

with open('SportZal.db','r', encoding ='utf-8-sig') as file_damp:
    damp = file_damp.read()

connection.executescript(damp)
connection.commit()

print("{:.^50}".format("DB created"))

connection.close()
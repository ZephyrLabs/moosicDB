from sys import exec_prefix
from modules.tui import tui
import sqlite3
from tabulate import tabulate

def addentry(db_handle):
    user_hash = input(tui.cfmt("Enter your unique hash (32 bytes): ", 1, 0, "red"))
    music_hash = input(tui.cfmt("Enter the song file hash (32 bytes): ", 1, 0, "blue"))
    music_name = input(tui.cfmt("Enter the song name: ", 1, 0, "lime"))
    music_artist = input(tui.cfmt("Enter moosic artist: ", 1, 0, "blue"))
    
    query = "insert into moosic_tb values('{}', '{}', '{}', '{}');".format(user_hash, music_hash, music_name, music_artist)
    tui.flush(tui)
    
    try:
        db_handle.execute(query)
    except:
        print("Well that didn't work out! try again :(")
        input()
        tui.flush(tui)

def viewall(db_handle):
    db_handle.execute("select * from moosic_tb;")
    table = db_handle.fetchall()
    table.insert(0, ["user_hash", "music_hash", "music_name", "music_artist"])
    tui.cfmt("Moosic DB:")
    print(tabulate(table))

    input()
    tui.flush(tui)

def viewusr(db_handle):
    hash = input(tui.cfmt("Enter the unique hash (32 bytes): ", 1, 0, "lime"))
    query = "select * from moosic_tb where user_hash = '{}';".format(hash)
    db_handle.execute(query)
    table = db_handle.fetchall()
    table.insert(0, ["user_hash", "music_hash", "music_name", "music_artist"])

    if(table == []):
        print("not found! :(")
        input()
        tui.flush(tui)
        return None

    tui.cfmt("Moosic DB:")
    print(tabulate(table))
    input()
    tui.flush(tui)

def viewhash(db_handle):
    hash = input(tui.cfmt("Enter your music hash (32 bytes): ", 1, 0, "lime"))
    query = "select * from moosic_tb where music_hash = '{}';".format(hash)
    db_handle.execute(query)
    table = db_handle.fetchall()
    table.insert(0, ["user_hash", "music_hash", "music_name", "music_artist"])

    if(table == []):
        print("not found! :(")
        input()
        tui.flush(tui)
        return None

    tui.cfmt("Moosic DB:")
    print(tabulate(table))
    input()
    tui.flush(tui)

tui.flush(tui)
print(tui.cfmt("Welcome to moosicDB!", 1, 0, "orange"))

# setup database
db = sqlite3.connect("moosic.db")
db_handle = db.cursor()
db_handle.execute("create table if not exists moosic_tb("
                  "user_hash char(32) not null," 
                  "music_hash char(32) PRIMARY KEY not null,"
                  "music_name char(64) not null,"
                  "music_artist char(32) not null);")
db.commit()

while(1):
    opt = tui.menu(tui, "Select your option:", ("Add entry", "View music chain"))
    
    if(opt == "1"):
        addentry(db_handle)

    if(opt == "2"):
        print(tui.cfmt("moosic vieww:", 1, 0, "orange"))
        opt = tui.menu(tui, "Select your option:", ("All moosic", "From user", "From hash"))
        if(opt == "1"):
            viewall(db_handle)
            input()
        if(opt == "2"):
            viewusr(db_handle)
            pass
        if(opt == "3"):
            viewhash(db_handle)
    db.commit()

    if(opt == "exit"):
        quit(0)

# Author Kevin Donovan based on coursework from Andrew Beatty
# songDAO.py
# WSAA course project 2024

import mysql.connector
import dbconfig as cfg

class songDAO:
    connection=""
    cursor= ''
    host= ''
    user= ''
    password= ''
    database= ''
       
    def __init__(self):
        self.host=cfg.mysql['host']
        self.user=cfg.mysql['user']
        self.password=cfg.mysql['password']
        self.database=cfg.mysql['database']

    # makes a connection with the cursor
    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()

    def getAll(self):
        cursor = self.getcursor()
        sql="select * from song"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            returnArray.append(self.convertToDictionary(result))
        self.closeAll()
        return returnArray
    
    def findByID(self, id):
        cursor = self.getcursor()
        sql="select * from song where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, song):
        cursor = self.getcursor()
        sql="insert into song (Category, Title, Band, Singer, Year) values (%s,%s,%s,%s,%s)"
        values = (song.get("Category"), song.get("Title"), song.get("Band"), song.get("Singer"), song.get("Year"))
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def update(self, id, song):
        cursor = self.getcursor()
        sql="update song set Category=%s, Title=%s, Band=%s, Singer=%s, Year=%s where id = %s"
        print(f"update music {song}")
        values = (song.get("Category"), song.get("Title"), song.get("Band"), song.get("Singer"), song.get("Year"), id)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from song where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()
        
    def convertToDictionary(self, resultLine):
        attkeys=['id','Category','Title', "Band", 'Singer', 'Year']
        song = {}
        currentkey = 0
        for attrib in resultLine:
            song[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1
        return song
        
songDAO = songDAO()

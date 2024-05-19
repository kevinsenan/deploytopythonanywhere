# Author Kevin Donovan based on coursework from Andrew Beatty
# server.py 
# WSAA course project 2024

# Importing packages:
from flask import Flask, jsonify, request, abort 
from songDAO import songDAO

app = Flask(__name__, static_url_path='', static_folder = '.')

# Get all songs
@app.route('/Songs')
def getAll():
    results = songDAO.getAll()
    return jsonify(results)

#find by ID
@app.route('/Songs/<int:id>')
def findById(id):
    foundSong = songDAO.findByID(id)
    return jsonify(foundSong)
 
# create
@app.route('/Songs', methods = ['POST'])
def create():
    if not request.json:
        abort(400)
    song = {
        "Category": request.json["Category"],
        "Title": request.json["Title"],
        "Band": request.json["Band"],
        "Singer": request.json["Singer"],
        "Year" : request.json["Year"]
    }
    addedsong = songDAO.create(song)
    return jsonify(addedsong)

# update
@app.route('/Songs/<int:id>', methods = ['PUT'])
def update(id):
    foundsong = songDAO.findByID(id)
    if not foundsong:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Year' in reqJson and type(reqJson['Year']) is not int:
        abort(400)
    if 'Category' in reqJson:
        foundsong['Category'] = reqJson['Category']
    if 'Title' in reqJson:
        foundsong['Title'] = reqJson['Title']
    if 'Band' in reqJson:
        foundsong['Band'] = reqJson['Band']
    if 'Singer' in reqJson:
        foundsong['Singer'] = reqJson['Singer']
    if 'Year' in reqJson:
        foundsong['Year'] = reqJson['Year']
    songDAO.update(id,foundsong)
    return jsonify(foundsong)

#delete
@app.route('/Songs/<int:id>', methods = ['DELETE'])
def delete(id):
    songDAO.delete(id)
    return jsonify({"done":True})

if __name__ == "__main__":
    app.run(debug = True)

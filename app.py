from flask import Flask, jsonify, request ,render_template
from data import data as db

app = Flask(__name__)

@app.route('/', methods=['GET'])
def Help():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def GetData():
    
    response = jsonify(db)
    return response, 200

@app.route('/data/<string:name>', methods=['GET'])
def GetDataFilterbyName(name):
    
    datafilter = [n for n in db if n['nome'] == name]
    
    if len(datafilter) == 0:
        return 'NAME NOT FOUND IN DATA', 403
    
    return jsonify(datafilter), 200

@app.route('/data/<int:id>', methods=['GET'])
def GetDataFilterbyID(id):
    
    datafilter = [i for i in db if i['id'] == id]
    
    if len(datafilter) == 0:
        return 'ID NOT FOUND IN DATA', 403
    
    return jsonify(datafilter), 200

@app.route('/send', methods=['POST'])
def SendData():
    
    NewPerson = request.get_json()
    
    for i in db:
        if i['id'] == NewPerson['id']:
            return 'ERRO ID NOT VALID', 404
        
    db.append(NewPerson)
    return jsonify(db), 201


@app.route('/edit/<int:id>', methods=['PUT'])
def Edit(id):
    
    info = request.get_json()
    
    for i in db:
        if i['id'] == id:
            i['nome'] = info['nome']
            i['idade'] = info['idade']
            return jsonify(db), 201
        
    return 'ERROR', 403

@app.route('/delete/<int:id>', methods=['DELETE'])
def Del(id):
    for i in db:
        if i['id'] == id:
            db.remove(i)
            return jsonify(db), 201
        
    return 'ERROR ID NOT FOUND'

if __name__ == '__main__':
    app.run(debug=True)
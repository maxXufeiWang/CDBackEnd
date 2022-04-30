from algEngine import *
from flask import Flask, jsonify, session, request
from flask_session import Session

from werkzeug.utils import secure_filename

engine = algEngine(".\\references")

app = Flask(__name__)
Session(app)

@app.route('/', methods=['GET'])
def hello_world(): 
    if request.method=='CONNECT':
        return "Stop"
    return "Dev Depolyment success."

@app.route('/file_upload',methods=['POST'])
def upload():
    if request.method=='CONNECT':
        return "Stop"
    if request.method == "POST":
        data = request.get_data()
        filename = data.decode().split("filename=")[1].split("\"")[1]
        ext = filename.split(".")[1]
        
        if ext != "txt":
            return jsonify({"code": 123, "msg": "Wrong file type"})

    
    return jsonify(engine.process_upload(data))


from flask import Flask, jsonify, session, request
from flask_session import Session

from werkzeug.utils import secure_filename

from utility.requestHandler import *
from utility.deleteTempFiles import *
from algEngine import *

import shutil


app = Flask(__name__)
Session(app)

engine = algEngine(".\\references")

base_dir  = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = base_dir


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/file_upload',methods=['POST'])
def upload():
    if request.method=='CONNECT':
        return "Stop"
    if request.method == "POST":
        data = handle(request.files.get('userUpload'), request.form.to_dict())

        if data['type'] == 'string':
            if "https://github.com" not in data['content']:
                return "Failed. It is not a github repo address."
            lst = process(data)
            deleteTempFiles(data['sessionID'])

            print(len(lst))

        
        elif data['type'] == 'application/zip':
            data['content'] = save(request.files.get('userUpload'), data['sessionID'])
            lst = process(data)
            deleteTempFiles(data['sessionID'])
            print(len(lst))

        elif data['type'] == 'application/octet-stream':
            local_dir = os.path.join(base_dir, 'storage')
            dir = os.path.join(local_dir, data['sessionID'])
            if not os.path.exists(dir):
                os.makedirs(dir) 
                with open(dir + "/temp.txt", 'wb') as f:
                    content = request.files.get('userUpload').read()
                    f.write(content)
                    f.close()
                data['content'] = dir
                lst = process(data)
                deleteTempFiles(data['sessionID'])

                print(len(lst))
            else:
                return "Failed. SessionID has been token by earlier access. "

        elif data['type'] == 'text/plain':
            print("=============================123123")
            local_dir = os.path.join(base_dir, 'storage')
            dir = os.path.join(local_dir, data['sessionID'])
            print(dir)
            if not os.path.exists(dir):
                os.makedirs(dir) 
                with open(dir + "/temp.txt", 'wb') as f:
                    content = request.files.get('userUpload').read()
                    f.write(content)
                    f.close()
                data['content'] = dir
                lst = process(data)
                deleteTempFiles(data['sessionID'])

                print(len(lst))
            else:
                return "Failed. SessionID has been token by earlier access. "

    return jsonify(engine.process_upload(lst))


def save(file, sessionID):
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # save zip

        local_dir = os.path.join(base_dir, 'storage')  
        dir = os.path.join(local_dir, sessionID)  # path for zip file

        temp = os.path.join(base_dir, filename)  # path for zip file
        shutil.unpack_archive(filename=hh, extract_dir=dir)# unzip and save

        os.remove(temp) # delete zip file


    return local_dir

if __name__ == '__main__':
    app.run()
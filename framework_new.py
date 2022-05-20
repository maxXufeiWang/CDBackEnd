from flask import Flask, jsonify, session, request, send_from_directory
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
    return 'Deployed.'

@app.route('/download',methods=['GET'])
def download():
    print(request)
    data = request.form.to_dict()
    sessionID = data['sessionID']
    #sessionID = "22011121"
    if os.path.exists('cryptoes\\' + sessionID + ".crypto"):
        try: 
            return send_from_directory('cryptoes\\', sessionID + ".crypto", as_attachment = True)
        except:
            return jsonify({"code": 404, "msg": "Failed. No record found."})

@app.route('/file_upload',methods=['POST'])
def upload():
    print('\n===================================================================================== \n')
    print('New API calling initiated.')
    if request.method=='CONNECT':
        return "Stop"
    if request.method == "POST":
        data = handle(request.files.get('userUpload'), request.form.to_dict())

        if data['type'] == 'string':
            if "https://github.com" not in data['content']:

                print('Terminated with error.')
                print('It is not a github repo address.')

                return jsonify({"code": 100, "msg": "Failed. It is not a github repo address."})

        elif data['type'] == 'application/zip':
            data['content'] = save(request.files.get('userUpload'), data['sessionID'])

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

            else:
                print('Terminated with error.')
                print('SessionID has been token by earlier access.')

                return jsonify({"code": 202, "msg": "Failed. SessionID has been token by earlier access. "})

        elif data['type'] == 'text/plain':
            local_dir = os.path.join(base_dir, 'storage')
            dir = os.path.join(local_dir, data['sessionID'])
            if not os.path.exists(dir):
                os.makedirs(dir) 
                with open(dir + "/temp.txt", 'wb') as f:
                    content = request.files.get('userUpload').read()
                    f.write(content)
                    f.close()
                data['content'] = dir

            else:
                print('Terminated with error.')
                print('SessionID has been token by earlier access.')

                return jsonify({"code": 202, "msg": "Failed. SessionID has been token by earlier access. "})

        else:
            print('Terminated with error.')
            print('Wrong file type')

            return jsonify({"code": 123, "msg": "Wrong file type"})

        lst = process(data, base_dir)

        deleteTempFiles(data['sessionID'])

        
        print('Found ', end='')
        print(len(lst), end='')
        print(' libraries.')

    print('\n===================================================================================== \n')

    return jsonify(engine.process_upload(lst))


def save(file, sessionID):
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # save zip

        local_dir = os.path.join(base_dir, 'storage')  
        dir = os.path.join(local_dir, sessionID)  # path for zip file

        temp = os.path.join(base_dir, filename)  # path for zip file
        shutil.unpack_archive(filename=temp, extract_dir=dir)# unzip and save

        os.remove(temp) # delete zip file


    return local_dir

if __name__ == '__main__':
    app.run()
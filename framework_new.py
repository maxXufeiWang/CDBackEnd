from flask import Flask, jsonify, session, request, send_file, send_from_directory
from flask_session import Session
from flask_cors import CORS

from werkzeug.utils import secure_filename

from utility.requestHandler import *
from utility.deleteTempFiles import *
from algEngine import *

import shutil
import pdfkit

app = Flask(__name__)
Session(app)
CORS(app, supports_credentials=True)
engine = algEngine(".\\references")

base_dir  = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = base_dir


@app.route('/')
def hello_world():
    return 'Deployed.'

@app.route('/download',methods=['POST'])
def download():
    data = request.data.decode()
    if "sessionID=" in data:
        sessionID = data.split("sessionID=")[1]
        if os.path.exists('txt\\' + sessionID + ".txt"):
            print('txt\\' + sessionID + ".txt")
            try: 
                print("success")
                return send_file('txt\\' + sessionID + ".txt", as_attachment = False)
            except:
                return jsonify({"code": 404, "msg": "Failed. No record found."})
    else:
        return jsonify({"code": 201, "msg": "No sessionID found"})

@app.route('/downloadpdf',methods=['POST'])
def downloadpdf():
    data = request.data.decode()
    if "sessionID=" in data:
        sessionID = data.split("sessionID=")[1]
        if os.path.exists('txt\\' + sessionID + ".txt"):
            with open('txt\\' + sessionID + ".txt", 'r') as myfile:
                data = myfile.read() 
                print(data)
                print(type(data))
                path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                pdfkit.from_string(data.encode('ascii', 'ignore').decode('ascii'), 'pdf\\' + sessionID + '.pdf', configuration=config)

            try: 
                print("correct")
                return send_from_directory('pdf\\', sessionID + ".pdf", as_attachment = False)
            except:
                return jsonify({"code": 404, "msg": "Failed. No record found."})
    else:
        return jsonify({"code": 201, "msg": "No sessionID found"})


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

        generateTXT(lst, data['sessionID'])

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

def generateTXT(lst, sessionID):
    s = "Identified Libraries:\n\n"

    for lib in lst:
        s = s + lib + "\n"

    with open('txt\\' + sessionID + ".txt", 'wt') as out:
        print(s, file=out)

if __name__ == '__main__':
    app.run()
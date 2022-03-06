from tokenize import Name
from algEngine import *
from flask import Flask, render_template, jsonify, session, request
from flask_session import Session

import shutil
import os
from werkzeug.utils import secure_filename
import pymysql
import redis

app = Flask(__name__)

base_dir  = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = base_dir

ALLOWED_EXTENSIONS = set(['zip'])

def allowed_file(filename): 
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

Session(app)

db = pymysql.connect(host="localhost", user="root", db="maxWang", password="sinocbd", port=3306)
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)


file_dir = './upload'

@app.route('/files_upload', methods=['POST'])
def upload_zip():  
    if request.method=='POST':
        file = request.files.get('files')

        if file.filename.rsplit('.')[-1] not in ['zip',]:
            path=os.path.join(base_dir,file.filename)
            with open(path,'w')as f:
                for line in file:
                    f.write(line.decode('utf-8'))
            with open(path,'rb')as f:
                count=0
                while True:
                    line = f.readline()
                    if line:
                        count+=1
                    else:
                        break
            sql='select id from user where user.user="'+session.get('user')+'"'
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.execute("INSERT into detail(user_id,lens) VALUES('"+str(data[0]['id'])+"','"+str(count)+"')")

            db.commit()

        # 处理压缩文件
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # save zip
            local_dir = os.path.join(base_dir, 'storage')  # create path for zip file
            hh = os.path.join(base_dir, filename)  # path for zip file
            shutil.unpack_archive(filename=hh, extract_dir=local_dir)# unzip and save

            os.remove(hh) # delete zip file

            filename = filename.split('.')[0]
            host_path = os.path.join(local_dir, filename)

            nameLst = engine.get_file_name(host_path)

            fileLst = get_files_rec(host_path, nameLst)
            
    return jsonify(engine.process_upload_zip(fileLst))

def get_files_rec(host_path, nameLst):
    dirLst = []

    for name in nameLst:
        new_path = os.path.join(host_path, name)
        if(os.path.isdir(new_path)):
            dirLst = dirLst + get_files_rec(new_path, engine.get_file_name(new_path))
        else:
            dirLst.append(new_path)

    return dirLst

@app.route('/file_upload',methods=['POST'])
def upload():
    if request.method == "POST":
        data = request.get_data()
    
    return jsonify(engine.process_upload(data))

if __name__ ==  '__main__':
    engine = algEngine(".\\backend\\references")
    app.run(host='0.0.0.0',port=8001)
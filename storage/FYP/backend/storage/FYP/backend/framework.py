from algEngine import *
from flask import Flask, render_template, jsonify, session, request
from flask_session import Session

import shutil
import os
from werkzeug.utils import secure_filename
import pymysql
import redis
import datetime
import time


app = Flask(__name__)

base_dir  = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = base_dir

ALLOWED_EXTENSIONS = set(['zip'])#允许文件上传的格式

def allowed_file(filename): # 判断上传文件的格式
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

# session存储到redis注册到flak中
Session(app)

# 建立pymysql连接
db = pymysql.connect(host="localhost", user="root", db="maxWang", password="sinocbd", port=3306)
# 使用cursor()方法创建一个游标对象
cursor = db.cursor(cursor=pymysql.cursors.DictCursor)


file_dir = './upload'

@app.route('/files_upload', methods=['POST'])
def upload_zip():  
    if request.method=='POST':
        file = request.files.get('files')

        print(file.filename)
        print(file.filename.rsplit('.')[-1])
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
            print(count)
            sql='select id from user where user.user="'+session.get('user')+'"'
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data[0])
            ctime=datetime.datetime.now()
            cursor.execute("INSERT into detail(user_id,lens) VALUES('"+str(data[0]['id'])+"','"+str(count)+"')")

            db.commit()

        # 处理压缩文件
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 压缩文件保存在项目路径下
            local_dir = os.path.join(base_dir, '11')  # 新创建一个路径，用来放压缩后的文件
            hh = os.path.join(base_dir, filename)  # 这个是找到压缩文件路径-------C:/Code/haha.zip
            print(hh)
            print(local_dir)
            shutil.unpack_archive(filename=hh, extract_dir=local_dir)# 把文件保存在刚刚设定好的路径下

            os.remove(hh) # 最后把压缩文件删除

            filename = filename.split('.')[0]
            print(filename)  # 此处为验证信息
            host_path = os.path.join(local_dir, filename+'.py')  # host.txt的路径
            print(host_path)
            with open(host_path, 'r',encoding='utf-8') as f:  # 把host文件打开
                key, values = [i.replace('\n', '').split(',') for i in f.readlines()]  # 列表推倒式，生成一个由键组成的列表，一个由值组成的列表
                hostvalue = dict(zip(key, values))  # 把两个列表组成字典
                print(hostvalue)
            ip = hostvalue['host_os_ip']  # 开始读取里面的信息
            systemname = hostvalue['host_database_bussines']
            databasename = hostvalue['host_database_instance']
            uploadtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(ip, systemname, databasename, uploadtime)


    return render_template('upload.html')



@app.route('/file_upload',methods=['POST'])
def upload():
    if request.method == "POST":
        data = request.get_data()
    
    return jsonify(engine.process_upload(data))

if __name__ ==  '__main__':
    engine = algEngine(".\\backend\\references")
    app.run(host='0.0.0.0',port=8001)
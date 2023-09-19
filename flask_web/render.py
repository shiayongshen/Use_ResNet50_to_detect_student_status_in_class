# save this as app.py
from flask import Flask, render_template, request, redirect, session,  Response,stream_with_context
import pymysql
import traceback
import datetime
import socket
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.utils import load_img
import time
import socket
#import mysql.connector
import datetime
app = Flask(__name__)

db = pymysql.connect(host="localhost", user="root", password="", database="rppgweb",charset="utf8")
# 創建表情類別
classes = ["confuse", "happy", "normal", "sleepy"]
def generate_frames():
    # 获取本机IP地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

# 載入模型
    resnet_model = hub.KerasLayer("https://tfhub.dev/tensorflow/efficientnet/b0/feature-vector/1")
    model = tf.keras.models.load_model("static/my_model.h5", custom_objects={'KerasLayer': hub.KerasLayer})
    # 創建 cursor 物件
    mycursor = db.cursor()
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FPS, 1)
    # 初始化結果陣列
    prediction_array = [[] for _ in range(10)]

    while True:
        success, frame = camera.read()  # 讀取攝像鏡頭畫面
        if not success:
            break
        else:
            # 將畫面轉換為灰度圖
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            # 使用OpenCV內建的人臉偵測器檢測人臉位置
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                    face_img = frame[y:y+h, x:x+w]
                    resized = cv2.resize(face_img, (224, 224))
                    img_array = img_to_array(resized)
                    img_array = img_array / 255.0
                    img_tensor = tf.convert_to_tensor(img_array)
                    img_tensor = tf.expand_dims(img_tensor, 0)
                    predictions = model.predict(img_tensor)
                    prediction = np.argmax(predictions)
                    prediction_array[len(prediction_array) - 1].append(prediction)
                    print(len(prediction_array[len(prediction_array) - 1]))
                    if len(prediction_array[len(prediction_array) - 1]) == 10:
                        flatten_array = np.concatenate(prediction_array).flatten().astype(int)
                        mode_prediction = np.argmax(np.bincount(flatten_array))
                        print(classes[mode_prediction])
                        currentDateAndTime = datetime.datetime.now()
                        currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
                        # 将预测结果和IP地址插入数据库中
                        sql = "INSERT INTO face_data (tip, face,dataTime) VALUES (%s, %s, %s)"
                        val = (ip_address, classes[mode_prediction],currentTime)
                        mycursor.execute(sql, val)
                        print(val)
                        # 提交更改
                        db.commit()
                        prediction_array = [[] for _ in range(10)]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, classes[prediction], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 輸出 JPEG 圖片

@app.route("/")
def home():
    return render_template('HomePage.html')
@app.route("/login")
def login():
    return render_template('StudentLogin.html')
@app.route("/teacherlogin")
def teacherlogin():
    return render_template('TeacherLogin.html')
@app.route("/teacherselect",methods = ['POST'])
def teacherselect():
    tid = request.values['tid']
    tpassword = request.values['tpassword']
    if tid and tpassword:
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM teacher WHERE tid = %s and tpassword = %s"
        try:
            # 执行sql语句
            cursor.execute(sql, (tid, tpassword))
            results = cursor.fetchall()
            if len(results) == 1:
                return redirect('/teacherShowLogin')
            else:
                return render_template('TeacherLogin.html',error_msg='用戶名或密碼不正確')
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()
        # 关闭数据库连接
        #db.close()
    else:
        return render_template('TeacherLogin.html',error_msg='請填寫用戶名')

@app.route("/teacherShowLogin")
def teacherShowLogin():
    cursor = db.cursor()
    sql = "SELECT id, name, time, login FROM students"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.commit()
    students = [{'id': r[0], 'name': r[1], 'time': r[2], 'login': r[3]} for r in results]
    
    return render_template('Teacher_show_login.html', students=students)

@app.route("/Teacher_show_data")
def Teacher_show_data():
    cursor = db.cursor()
    sql = "SELECT id, name, time, face, rppg FROM students S JOIN face_data F JOIN data D ON S.tip = F.tip and S.tip = D.tip"
    #sql = "SELECT id, name, time, face, rppg FROM students S JOIN face_data F ON S.tip = F.tip JOIN data D ON S.tip = D.tip ORDER BY time DESC LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.commit()
    students = [{'id': r[0], 'name': r[1], 'time': r[2], 'face': r[3], 'rppg' : float(r[4])} for r in results]
    print(students)
    return render_template('Teacher_show_data.html', students=students)



@app.route("/StudentRegister")
def StudentRegister():
    return render_template('StudentRegister.html')
@app.route("/register", methods=["POST"])
def register():
     # 获取本机IP地址
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    currentDateAndTime = datetime.datetime.now()
    currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
    # 将预测结果和IP地址插入数据库中
    id = request.values['id']
    name = request.values['name']
    password = request.values['password']
    if id and password:

        # 连接数据库,此前在数据库中创建数据库TESTD
        
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT id FROM students WHERE id =%s"
        # 执行sql语句
        cursor.execute(sql, (id))
        results = cursor.fetchall()
        if not results:
            sql2 = "INSERT INTO students(id,name,password,time,login,tip) VALUES(%s,%s,%s,%s,0,%s)"
            cursor.execute(sql2, (id,name,password,currentTime,ip_address))
            #results2 = cursor.fetchall()
            db.commit()
            return render_template('HomePage.html',error_msg='註冊成功!')
            # 提交到数据库执行
        else:
            return render_template('StudentRegister.html',error_msg='已經註冊過!')
    else:
        return render_template('StudentRegister.html',error_msg='請輸入學號密碼')



    
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/studentselect', methods=["POST"])
def getLoginRequest():
    # 獲取IP
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    # 获取表单数据
    id = request.values['id']
    password = request.values['password']
    
    if id and password:

        # 连接数据库,此前在数据库中创建数据库TESTD
        
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM students WHERE id = %s and password = %s"
        try:
            # 执行sql语句
            cursor.execute(sql, (id, password))
            results = cursor.fetchall()
            if len(results) == 1:
                currentDatetime = datetime.datetime.now()
                currentTime = currentDatetime.strftime("%Y-%m-%d %H:%M:%S")
                #session['is_login']= True      #返回需要跳转的页面或需要显示的字符串
                #print (currentTime)
                #print (ip_address)
                sql2 = "UPDATE students SET login = 1 WHERE id = %s"
                cursor.execute(sql2, (id))
                #results1= cursor.fetchall()
               # print (len(results1))
                sql3 = "UPDATE students SET time = %s WHERE id = %s"
                cursor.execute(sql3, (currentTime,id))
                sql4 = "UPDATE students SET tip = %s WHERE id = %s"
                cursor.execute(sql4, (ip_address,id))
                db.commit()
                return redirect('/video_feed')
                

            else:
                return render_template('StudentLogin.html',error_msg='用戶名或密碼不正確')
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            traceback.print_exc()
            db.rollback()
        # 关闭数据库连接
        #db.close()
    else:
        return render_template('StudentLogin.html',error_msg='請填寫用戶名')
@app.route("/studentcam")
def studentcam():
    return render_template('studentcam.html')
@app.route('/time')
def time():
    return Response(stream_with_context(start_time()))

def start_time():
    while True:
        now = datetime.datetime.now()
        yyyy = str(now.year)
        MM = str(now.month)
        dd = str(now.day)
        hh = str(now.hour)
        mm = str(now.minute)
        ss = str(now.second)
        day = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][now.weekday()]

        if int(hh) < 10:
            hh = "0" + hh
        if int(mm) < 10:
            mm = "0" + mm
        if int(ss) < 10:
            ss = "0" + ss

        date_time = f"{yyyy}/{MM}/{dd} {hh}:{mm}:{ss} {day}"
        yield date_time
        time.sleep(1)
@app.route("/end")
def end():
    cursor = db.cursor()
    sql = "UPDATE students SET login = 0"
    cursor.execute(sql)
    results = cursor.fetchall()
    db.commit()
    return render_template('HomePage.html')

if __name__ == '__main__':
    app.run(debug=True)
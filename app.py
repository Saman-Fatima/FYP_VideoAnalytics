from flask import Flask,render_template,request

from flask_mysqldb import MySQL
import datetime
import base64

import os
import numpy as np

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '2rmGIbqsnj'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'person_counter'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def customers():
    cur = mysql.connection.cursor()
    curG = mysql.connection.cursor()
    r=cur.execute("SELECT ABS(moved_IN-moved_Out) AS 'Persons', timestampp FROM customers Order by Sr DESC LIMIT 1 ")
    gg = curG.execute("SELECT male AS 'Males',female AS 'Females' FROM genderData Order by Sr DESC LIMIT 1 ")
    ##zaroon's
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()
    cur3 = mysql.connection.cursor()
    cur4 = mysql.connection.cursor()
    #print("aa")
    x=cur1.execute("SELECT ABS(moved_IN-moved_Out) AS 'Persons',timestampp FROM `customers` Order by Sr ASC")
    peak=cur2.execute("SELECT MAX(moved_IN) AS 'Persons',timestampp FROM `customers` WHERE timestampp >=now()-INTERVAL 30 DAY ")
    ID = cur4.execute("SELECT Sr FROM heatmap Order by Sr DESC LIMIT 1 ")
    h=cur3.execute("SELECT Photo FROM heatmap Order by Sr DESC LIMIT 1 ".format(str(ID)))
    myresult2=cur3.fetchall()

    StoreFIlePath="picc100.jpg".format(str(ID))
    #print(myresult2)
    with open(StoreFIlePath,'wb') as File:
        #File.write(myresult2)
        File.close()
    #plt.xlabel('Product Id')
    #plt.ylabel('Items in cart(number)')

    #print(myresult2[0]['Photo'])
    data = base64.b64decode(myresult2[0]['Photo'])
    #print(data)
    image_64_decode = base64.decodebytes(myresult2[0]['Photo'])
    image_result = open('pop.png', 'wb')  # create a writable image and write the decoding result
    image_result.write(image_64_decode)
    rows=(cur1.fetchall())
    pp=cur2.fetchall()
    print(type(rows))
    values=[]
    labels=[]
    for i in range(0,len(rows)):
        values.append(rows[i]['Persons'])
        labels.append(rows[i]['timestampp'])
        print(values[i])


    #for i in rows:
    #   print(i)

    #print(rows)

    peoplef=os.path.join('static','people_photo')
    legend = 'Visitors'

    if r>0:
        myresult = cur.fetchall()
    if gg>0:
        myresultGender = curG.fetchall()
    #print(myresult)
    myr=datetime.datetime.now()
    #make array if there are multiple tuples
    full_filename=os.path.join(peoplef,'pico1100.jpg')
    return render_template('cust.html',values=values, labels=labels, legend=legend,myresult=myresult[0]['Persons'],pinn=myresult[0]['timestampp'],myresultGender=myresultGender[0]['Males'],pinnG=myresultGender[0]['Females'],myr=myr,valuesPeople=values,labelsPeople=labels,peak=pp[0]['Persons'],peakt=pp[0]['timestampp'],user_image=full_filename,hp=myresult2[0]['Photo'])
if __name__=='__main__':
    app.run(debug=True)

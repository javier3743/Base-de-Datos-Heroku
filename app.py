from flask import Flask, request
from flask import render_template
import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
            dbname= dbname,
            user= user,
            password= password,
            host= host,
            port= port
            )





app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/magnet', methods = ['GET', 'POST'] )
def downmagnet ():
    if request.method == 'POST':
        idb = request.form['idbox']
        if idb == '':
            curD = conn.cursor()
            curD.execute("""SELECT * from magnetlink""")
            rows = curD.fetchall()
            return render_template('magnetlinks.html', rows = rows)
        curD = conn.cursor()
        curD.execute("""SELECT * from magnetlink where id = '""" + idb + """'""")
        row = curD.fetchall()
        urlrow = row[0][1]
        return render_template('result.html', result = urlrow)
    return render_template('query.html')

@app.route('/magnetup', methods = ['GET', 'POST'])
def upmagnet ():
    curU = conn.cursor()
    if request.method == 'POST':
        url =  request.form['urlbox']
        curU.execute("""INSERT INTO magnetlink (url) VALUES ( '""" + url +""" ' )""")
        curU.execute(""" COMMIT """)
        return render_template('successful.html')
    return render_template('upmagnet.html')






if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

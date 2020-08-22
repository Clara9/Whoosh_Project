from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import os.path
import string
from search_keys import Search

# from whoosh import fields
# from whoosh.fields import Schema, TEXT, ID
# from whoosh import index
# from whoosh.qparser import QueryParser

app = Flask(__name__)

# Database connection.
app.config['MYSQL_DATABASE_USER'] = 'whoosh'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'WhooshDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

#endpoint for search
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        # print(request.args)

        # kw = request.form['keyword']
        # if kw == None:
        s = Search()
        results, kw, df = "", "", ""
        flag = True
        if list(request.form) == ['keyword']:
            print("1")
            kw = request.form['keyword']
        elif list(request.form) == ['definition']:
            print("2")
            df = request.form['definition']
        if df == "":
            flag = True
        else:
            flag = False
        results = s.search2(df, kw, flag)

        return render_template('search.html', data = results)
    return render_template('search.html')

if __name__ == '__main__':
    app.debug = True
    # write_data()
    app.run(host='localhost',port=8000,debug=True)
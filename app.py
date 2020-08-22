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
            print(kw)
        elif list(request.form) == ['definition']:
            print("2")
            df = request.form['definition']
            print(df)
        if df == "":
            flag = True
        else:
            flag = False
        print(flag)

        results = s.search_terms(kw, df, flag)
        for r in results:
            print(r['title'])
            print(r['content'])
            print(r['subjective'])

        # What terms matched in each hit?
        print("matched terms")
        print("Number of matched result is " + str(len(results)))

        return render_template('search.html', data = results)
    return render_template('search.html')

if __name__ == '__main__':
    app.debug = True
    # write_data()
    app.run(host='localhost',port=8000,debug=True)

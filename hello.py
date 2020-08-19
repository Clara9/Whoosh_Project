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
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        # print(request.args)

        # kw = request.form['keyword']
        # if kw == None:
        s = Search()
        results = ""
        if list(request.form) == ['keyword']:
            print("1")
            kw = request.form['keyword']
            results = s.search(kw)
            print(kw)
            # print(results)
        if list(request.form) == ['definition']:
            print("2")
            df = request.form['definition']
            results2 = s.find_definition(df)
            if len(results2) > 20:
                results2 = results2[:20]
            print(df)
            # print(results)

        return render_template('search.html', data = results, data2 = results2)
    return render_template('search.html')

def write_data():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")

    schema = Schema(title=TEXT(stored=True), content=TEXT(stored = True))

    ix = index.create_in("indexdir", schema)

    writer = ix.writer()
    for i in range(len(titles)):
        writer.add_document(title = titles[i], content = texts[i])

    writer.commit()

if __name__ == '__main__':
    app.debug = True
    # write_data()
    app.run(host='https://whooshhproject.herokuapp.com',port=5000,debug=True)


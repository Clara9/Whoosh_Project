import mysql.connector

def connect_db(inputs):
    mydb = mysql.connector.connect(
        host="localhost",
        user="whoosh",
        password="123456",
        database="WhooshDB"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO Paper(title, text) VALUES (%s, %s)"
    delete_query = "DELETE FROM Paper"
    mycursor.execute(delete_query)

    cnt = 0
    for val in inputs:
        mycursor.execute(sql, val)
        cnt += 1
        # print(mycursor.rowcount, "record inserted.")
        mydb.commit()
    print(cnt)
    # print(mycursor.rowcount, "record inserted.")

def convert_data():
    with open('sample.txt') as f:
        texts = list(f)
    with open('sample-title.txt') as f2:
        titles = list(f2)

    res = []
    # print(len(texts))
    # print(len(titles))
    for i in range(len(texts)):
        res.append(tuple([titles[i][:-2], texts[i][:-2]]))
    # print(res)
    return res

def write_titles():
    with open('arxiv-titles-all.txt') as f2:
        titles = list(f2)
    titles = titles[:3000]
    f = open("sample-title.txt", "w")
    for t in titles:
        f.write(t)
    f.close()

def write_texts():
    with open('arxiv-abstracts-all.txt') as f2:
        titles = list(f2)
    texts = titles[:3000]
    f = open("sample.txt", "w")
    for t in texts:
        f.write(t)
    f.close()

# write_titles()
# write_texts()
connect_db(convert_data())



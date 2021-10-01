import xml.dom.minidom
import mysql.connector
import string
import sys
import datetime


def insert(cursor, state, cases, death, timestmp):
    print("In insert")
    cursor.execute("SELECT * FROM covdat")
    cursor.fetchall()
    rowc = cursor.rowcount

    if rowc != 51:
        query = "INSERT INTO covdat(State,Cases,Deaths,Time) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (state[: len(state) - 1], cases, death, str(timestmp)))
    else:
        print("GOING IN")
        update(cursor, state, cases, death, str(timestmp))


def update(cursor, state, cases, death, timestmp):
    query = "UPDATE covdat SET Cases=%s, Deaths=%s, Time=%s WHERE State=%s"
    cursor.execute(query, (cases, death, timestmp, state[: len(state) - 1]))


def update2(cursor, state, cases, death, timestmp):
    query = "UPDATE updcovdat SET Cases=%s, Deaths=%s, Time=%s WHERE State=%s"
    cursor.execute(query, (cases, death, timestmp, state[: len(state) - 1]))


arg1 = sys.argv[1]
# x = 0
# y = 0
# arg2 = sys.argv[2]
j = 0
currentT = datetime.datetime.now()
# currentT = str(currentT)
# populateCovdat = True
try:
    cnx = mysql.connector.connect(
        host="localhost", user="AGuy", password="[redacted]", database="CovCases"
    )
    cursor = cnx.cursor()
    cursor.execute("SELECT Time FROM covdat ORDER BY Time ASC LIMIT 1")
    x = cursor.fetchall()
    q = x[0][0]
    if q.date() < currentT.date():
        print("Updating previous dates")
        delquer = "DELETE FROM updcovdat"
        cursor.execute(delquer)
        cnx.commit()
        quer = "INSERT INTO updcovdat SELECT * FROM covdat"
        cursor.execute(quer)
        cnx.commit()
    doc1 = xml.dom.minidom.parse(arg1)

    # read the xml doc. Porting over to windows. This is just a template.
    table = doc1.getElementsByTagName("table")
    # print(len(table))
    for tr in table[0].getElementsByTagName(
        "tr"
    ):  # So, remember that when inspecting a source, its like a tree. You can access the child from the tree.
        # print(len(table[0].getElementsByTagName("tr")))
        data = []
        for td in tr.getElementsByTagName("td"):
            # use this x value to test tomorrow.
            # print(len(tr.getElementsByTagName("td")))
            vals = []

            for node in td.childNodes:

                if node.nodeType != node.TEXT_NODE:
                    # print("{} {}".format(x,y))
                    # print(td.getElementsByTagName("b")[0].childNodes[0].nodeValue)
                    # exit()
                    data.append(td.getElementsByTagName("b")[0].childNodes[0].nodeValue)
                    # print(vals)
            # print("Next iteration.")
            # y+=1
            # print(data)
            if len(data) == 3:
                # print(data)
                try:
                    data[0] = str(data[0])
                    data[1] = int(data[1].replace(",", ""))
                    # print(type(data[1]))
                    data[2] = int(data[2].replace(",", ""))
                    print(data)
                    j += 1
                    insert(cursor, data[0], data[1], data[2], currentT)
                    cnx.commit()
                    # print("Use the delta table which you will set up later. Mm.")
                    # print(x)

                except ValueError:
                    print("Invalid data")
                # data = []
        print("New iter")
        # x+=1

    print(data)
    cursor.close()

    data[0] = str(data[0])
    print(data)
    print(j)
except mysql.connector.Error as err:
    print(err)
finally:
    try:
        cnx
    except NameError:
        pass
    else:
        cnx.close()

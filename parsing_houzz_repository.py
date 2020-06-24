import mysql.connector
from mysql.connector import Error


def save(row):
    mydb = mysql.connector.connect(host='127.0.0.1',
                                   database='parsing-houzz',
                                   user='root',
                                   password='Wandex1',
                                   use_pure=True)
    try:

        mycursor = mydb.cursor()

        sql = "INSERT INTO images (imgFilename, imgCategory, imgIndex, color, pageNumber, parsedPage, imageColors) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (row["imgFilename"], row["imgCategory"], "1", "color", "1", "empty", row["imageColors"])
        mycursor.execute(sql, val)

        mydb.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (mydb.is_connected()):
            mydb.close()
            print("MySQL connection is closed")

# this means that if this script is executed, then
# main() will be executed
if __name__ == '__main__':
    save()

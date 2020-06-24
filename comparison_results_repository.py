import mysql.connector
from mysql.connector import Error


def get_comparison_results():
    try:
        cnx = mysql.connector.connect(host='94.130.73.202',
                                                  database='competitors_parser_kpb2',
                                                  user='kirill',
                                                  password='bp24os35if')
        sql_select_Query = """SELECT m.ourProductSku, m.parsedProductId, m.competitorLogin, oi.fileName AS ourImageFilename,
                                pi.fileName AS parsedImageFilename
                                FROM `matches` AS m
                                INNER JOIN `our_images` AS oi
                                ON oi.productSku = m.ourProductSku
                                INNER JOIN `parsed_images` AS pi
                                ON pi.productId = m.parsedProductId
                                WHERE m.comparisonResult = 10 AND m.parsedProductId IN (SELECT productId AS parsedProductId
                                FROM `parsed_images`
                                GROUP BY productId  
                                HAVINg count(productId) = 1)
                                LIMIT 200
"""
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in matches is - ", cursor.rowcount)
        '''
        for row in records:
            print("ourProductSku = ", row["ourProductSku"], )
            print("parsedProductId = ", row["parsedProductId"])
            print("competitorLogin  = ", row["competitorLogin"])
            print("ourImageFilename  = ", row["ourImageFilename"])
            print("parsedImageFilename  = ", row["parsedImageFilename"], "\n")
        '''
        cursor.close()
        return records
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (cnx.is_connected()):
            cnx.close()
            print("MySQL connection is closed")
            
def save(row):
    mydb = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                   database=os.getenv('DB_DATABASE'),
                                   user=os.getenv('DB_USERNAME'),
                                   password=os.getenv('DB_PASSWORD'),
                                   use_pure=True)
    try:

        mycursor = mydb.cursor()

        sql = "UPDATE adr (new_adr) VALUES (%s, %s, %s, %s)"
        val = (row["sku"], row["type"], row["color"], row["weight"])
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
    get_comparison_results()
import pymysql

connect = pymysql.connect(
     host="localhost",
     port=3306,
     user="root",
     passwd="xxxxxx",
     db="web_of_science"
)
def get_id_and_doi():
    # 返回一个字典，键->id，值->doi
    cursor = connect.cursor()
    cursor.execute("select unique_id,doi from wos_document;")
    result = cursor.fetchall()
    return dict(result)

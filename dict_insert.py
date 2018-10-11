import re
import pymysql


f = open('./dict.txt')

db = pymysql.connect('localhost','root','123456','dict1')

cursor = db.cursor()

l = []
for line in f:
    l = re.split(r'\s+',line)
    sql = "insert into words (word,jieshi) values \
            ('%s','%s')"%(l[0],' '.join(l[1:]))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

cursor.close()
f.close()
db.close()
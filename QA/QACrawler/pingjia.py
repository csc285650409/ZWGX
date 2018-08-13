#coding:utf8

import pymysql

dbname = 'zwgx'  # 数据库名
dbip = '106.14.124.221'  # 数据库IPlocalhost
dbport = 3306  # 数据库端口
dbusername = 'root'  # 数据库用户名
dbpassword = 'zwgx'  # 数据库密码root

def EXSQL(sql):
    try:
        db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname, charset="utf8")
        cursor = db.cursor()
        # sql = u"SELECT `学校名` FROM 学校简称 WHERE `简称`='" + w.word + "'"
        # 执行SQL语句
        cursor.execute(sql)
        if(not sql.__contains__("SELECT")):
            db.commit()
        # 获取所有记录列表
        results = cursor.fetchall()
        db.close()
        return results
    except Exception as e:
        print (e)


def InitSchool(schoolname,intention,s):
    for i in range(3):
        sql = u"INSERT INTO `问答预存` VALUES('"+schoolname+"','"+intention+"','"+i.__str__()+"','"+s+"','4','1','4')"
        EXSQL(sql)
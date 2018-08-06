#coding:utf8
# 导入EXCEL到MYSQL
import  pymysql
import xlrd

def ExceltoMySQL(excelpath,dbname,):

    # 打开数据库连接
    dbname = 'zwgx'  # 数据库名
    dbip = '106.14.124.221'  # 数据库IPlocalhost
    dbport = 3306  # 数据库端口
    dbusername = 'root'  # 数据库用户名
    dbpassword = 'zwgx'  # 数据库密码root
    try:
        # db = pymysql.connect("localhost", "root", "root", dbname,charset="utf8")
        db = pymysql.connect(host=dbip, user=dbusername, passwd=dbpassword, db=dbname, charset="utf8")
        cursor = db.cursor()
    except Exception as e:
        print(e)
        return

    # 获取表名
    if excelpath.rfind("\\")== -1:
        tablename=excelpath
    else:
        tablename=excelpath[excelpath.rfind("\\")+1:]
    if tablename.rfind(".")!= -1:
        tablename = tablename[:tablename.rfind(".")]


    #检查表存在？
    sql="SELECT COUNT(t.table_name) FROM information_schema.TABLES t WHERE t.table_name = '%s' AND t.TABLE_SCHEMA = '%s'" %(tablename,dbname)
    cursor.execute(sql)
    results = cursor.fetchall()
    if results[0][0]!=0:
        print("已存在表："+tablename)
        db.close()
        return

    # 建表
    excel = xlrd.open_workbook(excelpath)
    sheet = excel.sheet_by_index(0)
    col_names=[]
    for i in range(0,sheet.ncols):
        title=sheet.cell(0,i).value
        title=title.strip()
        title=title.replace(' ','_')
        col_names.append(title)
    sql="create table "+tablename+" (id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    for i in range(0,sheet.ncols):
        sql=sql+col_names[i]+" text"
        if i!=sheet.ncols-1:
            sql+=','
    sql =sql+")"
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
        db.close()
        return

    #插入数据
    sql="insert into "+tablename+" ("
    for i in range(0, sheet.ncols-1):
        sql = sql + col_names[i] + ', '
    sql = sql + col_names[sheet.ncols - 1]
    sql =sql+ ') values ('+ '%s,' * (sheet.ncols - 1)+ '%s)'
    ret=0
    parameter_list = []
    for row in range(1, sheet.nrows):
        for col in range(0, sheet.ncols):
            parameter_list.append(sheet.cell(row, col).value)
            # cell_type = sheet.cell_type(row, col)
            # cell_value = sheet.cell_value(row, col)
            # if cell_type == xlrd.XL_CELL_DATE:
            #     dt_tuple = xlrd.xldate_as_tuple(cell_value, file.datemode)
            #     meta_data = str(datetime.datetime(*dt_tuple))
            # else:
            #     meta_data = sheet.cell(row, col).value
            # parameter_list.append(meta_data)
        try:
            cursor.execute(sql, parameter_list)
            parameter_list = []
            ret += 1
            print("完成导入第：" + str(ret) + "条数据")
        except Exception as e:
            db.rollback()
            print(e)
    db.commit()
    db.close()
    print("完成导入表："+tablename+"\n导入数据："+str(ret))


# excelpath = r"C:\Users\csc88\Desktop\新建文件夹\school.xlsx"
# dbname="yihuiai"
# ExceltoMySQL(dbname=dbname,excelpath=excelpath)
if(__name__=='__main__'):
    # excelpath = input("输入文件地址")
    excelpath = r"C:\Users\csc88\Documents\WeChat Files\wxid_crut25q7oe6g21\Files\ss.xlsx"
    # dbname=input("输入数据库名")
    dbname='zwgx'
    ExceltoMySQL(dbname=dbname,excelpath=excelpath)


#coding:utf8

import aiml
import os
import pymysql
import sys
import json


reload(sys)
sys.setdefaultencoding('utf-8')
from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T
from QA.QACrawler import search_summary
from socket import socket, AF_INET, SOCK_STREAM

def initQA(mybot):
    # 初始化jb分词器
    T.jieba_initialize()

    # 切换到语料库所在工作目录
    mybot_path = './'
    os.chdir(mybot_path)


    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/std-startup.xml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/bye.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/tools.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/bad.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/funny.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/OrdinaryQuestion.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/QA/resources/Common conversation.aiml")
    mybot.respond('Load Doc Snake')
    # 载入百科属性列表
    print '''
    Frank：你好，我是Frank o(*≧▽≦)ツ
    '''

def QA(input_message,mybot):
    findAns = False
    reply=''
    ansdict={}
    dbname='zwgx' #数据库名
    dbip='localhost'#数据库IP
    dbusername='root'#数据库用户名
    dbpassword='root'#数据库密码
    if len(input_message) > 60:
        reply = mybot.respond("句子长度过长")
        findAns = True
    elif input_message.strip() == '无':
        reply = mybot.respond("无")
        findAns = True

    if (findAns == False):
        # print input_message
        message = T.wordSegment(input_message)
        # 分词去标点
        if message == 'q':
            exit()
        else:
            print 'word Seg:' + message
            print '词性：'
            words = T.postag(input_message)
            for w in words:
                print w.word, w.flag

                # 配对数据库中已存内容
                if w.flag == 'x' or w.flag == 'nt':
                    try:
                        db = pymysql.connect(dbip, dbusername, dbpassword, dbname, charset="utf8")
                        cursor = db.cursor()
                        sql=u"SELECT `属性`,`内容` FROM school WHERE `学校`='"+w.word+"'"
                        # 执行SQL语句
                        cursor.execute(sql)
                        # 获取所有记录列表
                        results = cursor.fetchall()
                        if len(results)>0:
                            for row in results:
                                ansdict[row[0]]=row[1]
                                # reply +=row[0].encode("utf8")
                                # reply+=" ".encode("utf8")
                            # shuxing=raw_input('Frank：你想了解什么属性 ' + reply+">>")
                            # sql = u"SELECT `内容` FROM school WHERE `学校`='" + w.word + u"'AND `属性`='"+shuxing+"'"
                            # cursor.execute(sql)
                            # results = cursor.fetchall()
                            # if len(results)>0:
                            #     print "Frank： "+results[0][0].encode("utf8")
                            #     reply=results[0][0].encode("utf8")
                            #     return reply
                            # 关闭数据库连接
                            db.close()
                    except Exception as e:
                        print(e)

            response = mybot.respond(input_message.strip())

            print "======="
            print response
            print "======="

            if response == "":
                reply = mybot.respond('找不到答案')
                findAns = True
                print 'Frank：' + reply

            # 百科搜索
            elif response[0] == '#':
                # 匹配百科
                if response.__contains__("searchbaike"):
                    print "searchbaike"
                    print response
                    res = response.split(':')
                    # 实体
                    entity = str(res[1]).replace(" ", "")
                    # 属性
                    attr = str(res[2]).replace(" ", "")
                    print entity + '<---->' + attr

                    ans = baike.query(entity, attr)
                    # 如果命中答案
                    if type(ans) == list:
                        print 'Frank：' + QAT.ptranswer(ans, False)
                        reply = QAT.ptranswer(ans, False)
                        findAns = True
                    elif ans.decode('utf-8').__contains__(u'::找不到'):
                        # 百度摘要+Bing摘要
                        print "通用搜索"
                        ans = search_summary.kwquery(input_message)

                # 匹配不到模版，通用查询
                elif response.__contains__("NoMatchingTemplate"):
                    print "NoMatchingTemplate"
                    ans = search_summary.kwquery(input_message)

                if (findAns == False):
                    if len(ans) == 0:
                        ans = mybot.respond('找不到答案')
                        print 'Frank：' + ans
                        reply = ans
                        findAns = True

                    elif len(ans) > 1:
                        print "不确定候选答案"
                        print 'Frank: '
                        for a in ans:
                            print a.encode("utf8")
                            reply += a.encode("utf8") + '\n'
                        findAns = True
                    else:
                        print 'Frank：' + ans[0].encode("utf8")
                        reply = ans[0].encode("utf8")
                        findAns = True

            # 匹配模版
            else:
                print 'Frank：' + response
                reply = response
                findAns = True

    ansdict['baidu']=reply
    json_s=json.dumps(ansdict)
    print json_s
    # return reply
    return json_s

if __name__ == '__main__':

    mybot = aiml.Kernel()
    initQA(mybot)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('127.0.0.1',50008))
    sock.listen(5)

    while True:

        # if(reply!=''):
        #     conn.send(reply)
        #     reply=''

        conn,addr = sock.accept()
        data = conn.recv(4096)
        input_message = data

        print "input_message====="
        print input_message
        print "=========="

        reply=QA(input_message,mybot)
        conn.send(reply)




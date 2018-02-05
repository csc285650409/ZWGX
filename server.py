#coding:utf8

import aiml
import os

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
            response = mybot.respond(input_message.strip())

            print "======="
            print response
            print "======="

            if response == "":
                reply = mybot.respond('找不到答案')
                findAns = True
                print 'Eric：' + reply

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
                        print 'Eric：' + QAT.ptranswer(ans, False)
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
                        print 'Eric：' + ans
                        reply = ans
                        findAns = True

                    elif len(ans) > 1:
                        print "不确定候选答案"
                        print 'Eric: '
                        for a in ans:
                            print a.encode("utf8")
                            reply += a.encode("utf8") + '\n'
                        findAns = True
                    else:
                        print 'Eric：' + ans[0].encode("utf8")
                        reply = ans[0].encode("utf8")
                        findAns = True

            # 匹配模版
            else:
                print 'Eric：' + response
                reply = response
                findAns = True

    return reply


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




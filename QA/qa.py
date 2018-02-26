#coding:utf8
import aiml
import os

from QA.QACrawler import baike
from QA.Tools import Html_Tools as QAT
from QA.Tools import TextProcess as T
from QACrawler import search_summary
import server


if(__name__=='__main__'):
    mybot = aiml.Kernel()
    server.initQA(mybot)

    while 1:
        input_message = raw_input("Enter your message >> ")
        try:
            server.QA(input_message,mybot)
        except:
            print '很抱歉啦，这个我也母鸡啊！'



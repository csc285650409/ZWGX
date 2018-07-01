#coding:utf8
import aiml
import os

import sys
sys.path.append("..")
import server




if(__name__=='__main__'):
    mybot = aiml.Kernel()
    server.initQA(mybot)

    while 1:
        input_message = raw_input("Enter your message >> ")
        server.QA(input_message, mybot)
        # try:
        #     server.QA(input_message,mybot)
        # except:
        #     print '很抱歉啦，这个我也母鸡啊！'



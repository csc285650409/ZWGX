#-*- coding: utf-8 -*-

def display():
	print("123")
dic = {1:"1",2:display,3:"3"}

if __name__ == '__main__':
	print dic[2]()
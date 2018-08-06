#coding:utf8

# import urllib
# import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

class Session:
    def __init__(self):
        self.session=requests.session()
    # session = requests.session()
    headers={'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
'''
获取百度知道的页面
'''
def get_html_zhidao(url,req):
    soup = BeautifulSoup(req.session.get(url=url, headers=req.headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup(['script', 'style','img'])]
    # print(soup.prettify())
    return soup

'''
获取百度百科的页面
'''
def get_html_baike(url,req):
    soup = BeautifulSoup(req.session.get(url=url, headers=req.headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup(['script', 'style', 'img', 'sup'])]
    # print(soup.prettify())
    return soup



'''
获取Bing网典的页面
'''
def get_html_bingwd(url,req):
    soup = BeautifulSoup(req.session.get(url=url, headers=req.headers).content, "lxml")

    # 去除无关的标签
    [s.extract() for s in soup(['script', 'style', 'img', 'sup'])]
    # print(soup.prettify())
    return soup



'''
获取百度搜索的结果
'''
def get_html_baidu(url,req):
    soup = BeautifulSoup(req.session.get(url=url, headers=req.headers).content, "lxml")
    # 去除无关的标签
    # [s.extract() for s in soup(['script', 'style','img'])]
    [s.extract() for s in soup(['style', 'img'])]
    # print(soup.prettify())
    return soup

def get_html_baidu_selenium1(schoolname,req):
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
    driver.get("https://gaokao.chsi.com.cn/sch/search.do?searchType=1&yxmc="+schoolname)
    soup = BeautifulSoup(driver.page_source,'lxml')
    soup = soup.find(class_="js-yxk-yxmc").find("a")["href"]
    soup = get_html_baidu("https://gaokao.chsi.com.cn" + soup,req)
    return soup

def get_html_baidu_selenium2(schoolname,req):
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
    driver.get("http://college.gaokao.com/schlist/n"+schoolname)
    soup = BeautifulSoup(driver.page_source,'lxml')
    soup = soup.find(class_="scores_List").find("dt").find("a")["href"]
    soup = get_html_baidu(soup,req)
    return soup




'''
获取Bing搜索的结果
'''
def get_html_bing(url,req):
    # url = 'http://global.bing.com/search?q='+word
    soup = BeautifulSoup(req.session.get(url=url, headers=req.headers).content, "lxml")

    # 去除无关的标签
    # [s.extract() for s in soup_bing(['script', 'style','img'])]
    return soup



# '''
# print answer
# '''
# def ptranswer(ans,ifhtml):
#     result = ''
#     # print ans
#     for answer in ans:
#         if ifhtml:
#             print answer
#         else:
#             if answer == u'\n':
#                 # print '回车'
#                 continue
#             p = re.compile('<[^>]+>')
#             # print '##############'
#             # print answer
#             # print type(answer)
#             # if answer.name == 'br':
#             #     continue
#             # print p.sub("", answer.string)
#             # print '##############'
#             result += p.sub("", answer.string).encode('utf8')
#     return result
#
#
# def ltptools(args):
#     url_get_base = "http://api.ltp-cloud.com/analysis/"
#     result = urllib.urlopen(url_get_base, urllib.urlencode(args)) # POST method
#     content = result.read().strip()
#     return content


if __name__ == '__main__':
    pass
    # get_html_baidu("http://baike.baidu.com/item/")
    # args = {
    #     'api_key' : 'F1e194G841HHvTDhqb4JsGrHHw4Q0DYFbzKqgQNm',
    #     'text' : '太阳为什么是圆的。',
    #     'pattern' : 'srl',
    #     'format' : 'json'
    # }
    # content = ltptools(args=args)
    # print content
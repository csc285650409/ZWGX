#coding:utf8

import time
from urllib import quote
from aip import AipNlp
from QA.Tools import Html_Tools as To
from QA.Tools import TextProcess as T
# import pynlpir

APP_ID = '11437411'
API_KEY = '2B6dy6KWVZhwd8cHdjd4Rp6B'
SECRET_KEY = 'qYu83SEnfzpwiFe0L9gmu2etpIneYBuA '

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

'''
对百度、Bing 的搜索摘要进行答案的检索
（需要加问句分类接口）
'''

def kwquery(query):
    #分词 去停用词 抽取关键词
    keywords = []
    # try:
    #     pynlpir.open()
    #     keywords = pynlpir.get_key_words(query, weighted=True)
    #     print "关键词："
    #     for key_word in keywords:
    #         print key_word[0], '\t', key_word[1]
    #     pynlpir.close()
    # except Exception as ex:
    #     print ex

    # words = T.postag(query)
    # for k in words:
    #     # 只保留名词
    #     if k.flag.__contains__("n"):
    #         # print k.flag
    #         # print k.word
    #         keywords.append(k.word)
    req=To.Session()
    # req.session.cookies.clear()
    answer = []
    text = ''
    # 找到答案就置1
    flag = 0


    # 抓取百度前10条的摘要
    soup_baidu = To.get_html_baidu('https://www.baidu.com/s?wd='+quote(query),req)
    #判断是否有两个id为1的页面
    if(soup_baidu.find_all(id = 1).__len__() > 1):
        results = soup_baidu.find_all(id = 1)[1]
        url = results.find("h3").find("a")['href']
        if url != None:
            baike_soup = To.get_html_baike(url, req)
            r = baike_soup.find(class_ = 'lemma-summary')
            if r != None:
                r = r.get_text().replace("\n", "").strip()
                if r != "":
                    answer.append(r)
                    flag = 1
    else:
        for i in range(1, 10):
            if soup_baidu == None:
                break
            results = soup_baidu.find(id = i)
            if results == None:
                # print "百度摘要找不到答案"
                continue
                # print '============='
                # print results.attrs
                # print type(results.attrs)
                # print results['class']
                # 判断是否有mu,如果第一个是百度知识图谱的 就直接命中答案
            if results.attrs.has_key('mu') and i == 1:
                # print results.attrs["mu"]
                r = results.find(class_ = 'op_exactqa_s_answer')
                if r == None:
                    pass  # print "百度知识图谱找不到答案"
                else:
                    # print r.get_text()
                    # print "百度知识图谱找到答案"
                    r = r.get_text().strip()
                    if r != "":
                        answer.append(r)
                        flag = 1
                        break

            # 百度百科
            # if results.find("h3").find("a").get_text().__contains__(u"百度百科") and (i == 1 or i ==2 or i==3):
            if results.find("h3").find("a").get_text().__contains__(u"_百度百科"):
                url = results.find("h3").find("a")['href']
                if url == None:
                    # print "百度百科找不到答案"
                    continue
                else:
                    # print "百度百科找到答案"
                    baike_soup = To.get_html_baike(url, req)

                    r = baike_soup.find(class_ = 'lemma-summary')
                    if r == None:
                        continue
                    else:
                        r = r.get_text().replace("\n", "").strip()
                        if r != "":
                            answer.append(r)
                            flag = 1
                            break

            # 古诗词判断
            if results.attrs.has_key('mu') and i == 1:
                r = results.find(class_ = "op_exactqa_detail_s_answer")
                if r == None:
                    pass  # print "百度诗词找不到答案"
                else:
                    # print r.get_text()
                    # print "百度诗词找到答案"
                    r = r.get_text().strip()
                    if r != "":
                        answer.append(r)
                        flag = 1
                        break

            # 万年历 & 日期
            if results.attrs.has_key('mu') and i == 1 and results.attrs['mu'].__contains__(
                    'http://open.baidu.com/calendar'):
                r = results.find(class_ = "op-calendar-content")
                if r == None:
                    pass  # print "百度万年历找不到答案"
                else:
                    # print r.get_text()
                    # print "百度万年历找到答案"
                    r = r.get_text().strip().replace("\n", "").replace(" ", "")
                    if r != "":
                        answer.append(r)
                        flag = 1
                        break

            if results.attrs.has_key('tpl') and i == 1 and results.attrs['tpl'].__contains__('calendar_new'):
                # r = results.attrs['fk'].replace("6018_","")
                if results.find(attrs = {"data-compress": "off"}):
                    r = results.find(attrs = {"data-compress": "off"}).get_text()
                    r = r[r.find('selectDate'):]
                    r = r[r.find('[') + 1:r.find(']')]
                    r = r.replace("\"", "")
                    r = r.split(',')

                # r=results.find(class_="op-calendar-new-right-date")
                # print r
                if r == None:
                    pass  # print "百度万年历新版找不到答案"
                    # continue
                else:
                    # print r.get_text()
                    # print "百度万年历新版找到答案"
                    r = r[0] + "年" + r[1] + "月" + r[2] + "日"
                    answer.append(r)
                    flag = 1
                    break

            if results.attrs.has_key('tpl') and i <= 2 and results.attrs['tpl'].__contains__('exactqa'):
                # r = results.attrs['fk'].replace("6018_","")
                r = results.find(class_ = "op_exactqa_s_prop c-gap-bottom-small")
                # print r.a

                if r == None:
                    pass  # print "百度黄历找不到答案"
                    # continue
                else:
                    r = r.a
                    # print "百度黄历找到答案"
                    answer.append(r.get_text())
                    flag = 1
                    break

            # 计算器
            if results.attrs.has_key('mu') and i == 1 and results.attrs['mu'].__contains__(
                    'http://open.baidu.com/static/calculator/calculator.html'):
                # r = results.find('div').find_all('td')[1].find_all('div')[1]
                r = results.find(class_ = 'op_new_val_screen_result')
                if r == None:
                    pass  # print "计算器找不到答案"
                    # continue
                else:
                    # print r.get_text()
                    # print "计算器找到答案"
                    r = r.get_text().strip()
                    if r != "":
                        answer.append(r)
                        flag = 1
                        break

            # 百度知道答案
            if results.attrs.has_key('mu') and i == 1:
                # print results.attrs["mu"]
                r = results.find(class_ = 'op_best_answer_question_link')
                if r == None:
                    r = results.find(class_ = 'op_generalqa_answer_title')
                    if r == None:
                        pass  # print "百度知道图谱找不到答案"
                    else:
                        r = r.a
                        # print "百度知道图谱找到答案"
                        url = r['href']
                        zhidao_soup = To.get_html_zhidao(url, req)
                        r = zhidao_soup.find(class_ = 'bd answer').find('pre')
                        if r == None:
                            continue
                        answer.append(r.get_text())
                        flag = 1
                        break
                else:
                    # print "百度知道图谱找到答案"
                    url = r['href']
                    zhidao_soup = To.get_html_zhidao(url, req)
                    r = zhidao_soup.find(class_ = 'bd answer')
                    if r == None:
                        continue
                    r = r.find('pre')
                    if r == None:
                        continue
                    answer.append(r.get_text())
                    flag = 1
                    break

            if results.find("h3") != None:
                # 百度知道
                if results.find("h3").find("a").get_text().__contains__(u"百度知道") and (i <= 5):
                    url = results.find("h3").find("a")['href']
                    if url == None:
                        # print "百度知道找不到答案"
                        continue
                    else:
                        # print "百度知道找到答案"
                        zhidao_soup = To.get_html_zhidao(url, req)

                        r = zhidao_soup.find(class_ = 'bd answer')
                        if r == None:
                            continue
                        r = r.find('pre')

                        if r == None:
                            continue
                        r = r.get_text().strip()
                        if r != "":
                            answer.append(r)
                            flag = 1
                            break

            text += results.get_text()

    if flag == 1:
        return answer
    else:
        results = soup_baidu.find(id = 1)
        if(results == None):
            answer.append(u"很抱歉，这个我也母鸡啊！")
        else:
            r = results.find(class_ = "c-abstract")
            [s.extract() for s in r(['span'])]
            answer.append(r.get_text())
    del req
    return answer
    # #获取bing的摘要
    # soup_bing = To.get_html_bing('https://www.bing.com/search?q='+quote(query),req)
    # # 判断是否在Bing的知识图谱中
    # # bingbaike = soup_bing.find(class_="b_xlText b_emphText")
    # bingbaike = soup_bing.find(class_="bm_box")
    #
    # if bingbaike != None:
    #     if bingbaike.find_all(class_="b_vList")[1] != None:
    #         if bingbaike.find_all(class_="b_vList")[1].find("li") != None:
    #             # print "Bing知识图谱找到答案"
    #             flag = 1
    #             answer.append(bingbaike.get_text())
    #             # print "====="
    #             # print answer
    #             # print "====="
    #             return answer
    # else:
    #     # print "Bing知识图谱找不到答案"
    #     results = soup_bing.find(id="b_results")
    #     bing_list = results.find_all('li')
    #     for bl in bing_list:
    #         temp =  bl.get_text()
    #         if temp.__contains__(u" - 必应网典"):
    #             # print "查找Bing网典"
    #             url = bl.find("h2")
    #             if url == None:
    #                 # print "Bing网典找不到答案"
    #                 continue
    #             url=url.find("a")
    #             if url == None:
    #                 # print "Bing网典找不到答案"
    #                 continue
    #             else:
    #                 # print "Bing网典找到答案"
    #                 url=url['href']
    #                 bingwd_soup = To.get_html_bingwd(url,req)
    #
    #                 r = bingwd_soup.find(class_='bk_card_desc')
    #                 if r == None:
    #                     continue
    #                 r=r.find("p")
    #                 if r == None:
    #                     continue
    #                 else:
    #                     r = r.get_text().replace("\n","").strip()
    #                 answer.append(r)
    #                 flag = 1
    #                 break
    #
    #     if flag == 1:
    #         return answer
    #
    #     text += results.get_text()

    # print text



    # # 如果再两家搜索引擎的知识图谱中都没找到答案，那么就分析摘要
    # if flag == 0:
    #     #分句
    #     cutlist = [u"。",u".",u"?",u"？", u"_", u"-",u":",u"：",u"！",u"!","\n"]
    #     temp = ''
    #     sentences = []
    #     for i in range(0,len(text)):
    #         if text[i] in cutlist:
    #             if temp == '':
    #                 continue
    #             else:
    #                 # print temp
    #                 sentences.append(temp)
    #             temp = ''
    #         else:
    #             temp += text[i]
    #
    #     # 找到含有关键词的句子,去除无关的句子
    #     key_sentences = {}
    #     for s in sentences:
    #         for k in keywords:
    #             if k[0] in s:
    #                 key_sentences[s]=1
    #
    #
    #     # 根据问题制定规则
    #
    #     # 识别人名
    #     target_list = {}
    #     for ks in key_sentences:
    #         # print ks
    #         words = T.postag(ks)
    #         for w in words:
    #             # print "====="
    #             # print w.word
    #             if w.flag == ("nr"):
    #                 if target_list.has_key(w.word):
    #                     target_list[w.word] += 1
    #                 else:
    #                     target_list[w.word] = 1
    #
    #     # 找出最大词频
    #     sorted_lists = sorted(target_list.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    #     # print len(target_list)
    #     #去除问句中的关键词
    #     sorted_lists2 = []
    #     # 候选队列
    #     for i, st in enumerate(sorted_lists):
    #         # print "1 "+st[0]
    #         # print st
    #         if st[0] in keywords:
    #             continue
    #         else:
    #             sorted_lists2.append(st)
    #
    #     print "返回前3个词频"
    #     answer = []
    #     for i,st in enumerate(sorted_lists2):
    #         # print st[0]
    #         # print st[1]
    #         if i< 3:
    #             # print st[0]
    #             # print st[1]
    #             answer.append(st[0])
    #     # print answer

if __name__ == '__main__':
    pass
    query1 = "北大在哪里"
    query2 = "上海交大的具体位置？"
    ans = kwquery(query1)
    print "~~~~~~~"
    for a in ans:
        print a
    print "~~~~~~~"
    # ans = client.simnet(query1,query2)
    # print ans.get("score")
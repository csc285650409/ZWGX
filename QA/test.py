#-*- coding: utf-8 -*-
import synonyms

# synonyms.display("地点")

# r = synonyms.seg("上海海事大学食堂有多远？")
# for i in r:
# 	for m in i:
# 		print m

sen1 = "北京工业大学"
sen2 = "北京工业大学耿丹学院"
print(sen1)
print(sen2)
r = synonyms.compare(sen1, sen2, seg=True)
print "相似度:",r
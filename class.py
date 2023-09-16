#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import time
import schedule
import re
import telegram
import sys

def tele(message):
    if message=='' :
        message='空值'
    bots=telegram.Bot("5329391020:AAH8dHkIRpwPxxhSfCiGWoCikpMkaW33EI8")
    bots.send_message(text=str(message), chat_id=1217566905)

file=open('/root/table/课表.html',encoding="utf-8")
ClassTab=file.read()
soup=BeautifulSoup(ClassTab, "html.parser")
file.close()
jie_ci=[]
jie_ci=jie_ci+list(map(int,sys.argv[1:len(sys.argv)]))

def auto(t,*info1):
    localtime = time.localtime(time.time())
    start_time=time.strptime('2023 8 28','%Y %m %d')
    for i in t:
        seed1=i['time']//1000 #课程星期数
        seed2=i['time']%1000  #课程节数
        if seed1 == localtime[6]+1 :
            if seed2 == info1[0][1] :
                for m in i['info']:
                    if (int(time.strftime('%W',localtime))-int(time.strftime('%W',start_time))+1) == m:
                        print(i['name']+'\n'+i['site'][7:]+'\n'+'周'+str(i['time']//1000)+'第'+str(i['time']%1000)+'节'+'\n'+i['teacher'][1:]
                        return i['name']+'\n'+i['site'][7:]+'\n'+'周'+str(i['time']//1000)+'第'+str(i['time']%1000)+'节'+'\n'+i['teacher'][1:]
def hand(t,*info1):
    txt=''
    for i in t:
        seed1=i['time']//1000 #课程星期数
        seed2=i['time']%1000  #课程节数
        if seed1 == info1[0][0] :
            if seed2 == info1[0][1] :
                for m in i['info']:
                    if info1[0][2] == m:
                        print(i['name']+'\n'+i['site'][7:]+'\n'+'周'+str(i['time']//1000)+'第'+str(i['time']%1000)+'节'+'\n'+i['teacher'][1:])
                        txt=txt+'\n'+i['name']+'\n'+i['site'][7:]+'\n'+'周'+str(i['time']//1000)+'第'+str(i['time']%1000)+'节'+'\n'+i['teacher'][1:]
    return txt

##name=课程名称
#site=上课地点
#teacher=上课老师
#credit=学分
#week=课程周数
#time=上课时间
#period=学时

table=[] ##课表数组，元素是字典{name,week,time,site,teacher,credit,period}

for w in [1,2,3,4,5,6,7]:
    for c in [1,2,3,4,5,6,7,8,9,10,11,12]:
        tag_id=str(w)+'-'+str(c)
        if soup.find(id=tag_id) is None:
            continue
        if soup.find(id=tag_id).contents == []:
            continue
        for div_tag in soup.find(id=tag_id).children:
            if div_tag.u is None :
                name=div_tag.span.font.string
            else:
                name=div_tag.u.font.string
##            print(tag_id,'\n******************************************************')
            time_code=w*1000+c
##            print(name)
            for i in div_tag.find('span',attrs={'title':'节/周'}).next_siblings:
##                print(i.string)
                week=i.string
            for i in div_tag.find('span',attrs={'title':'上课地点'}).next_siblings:
##                print(i.string)
                site=i.string
            for i in div_tag.find('span',attrs={'title':'教师'}).next_siblings:
##                print(i.string)
                teacher=i.string
            for i in div_tag.find('span',attrs={'title':'学分'}).next_siblings:
##                print(i.string)
                credit=i.string
            for i in div_tag.find('span',attrs={'title':'课程学时组成'}).next_siblings:
##                print(i.string)
                period=i.string 
            table=table+[{'name':name.replace(' ',''),'week':week.replace(' ',''),'time':time_code,'site':site,'teacher':teacher,'credit':credit,'period':period}]
##print(table)


for every_lesson in table:# i是每一节课的字典
    week1=[a for a in re.split('[(),+]',every_lesson['week']) if a] #切割课程week的值，保存到列表week1中 ，['5-6节', '1-4周', '7-11周']
    del week1[0] #删除节次，保留周数，['1-4周', '7-11周']
    info=[0]#创建周次列表，[1,2,3,4,5,6,11,12,13]
    for every_section in week1:
        weeked=[a for a in re.split('[-周]',every_section) if a]
        if len(weeked) == 1:
            info=info+list(map(int,weeked))
        else:
            info=info+list(range(int(weeked[0]),int(weeked[1])+1))
        every_lesson.update({'info':info})#往table添加info：[1, 2, 3, 4, 7, 8, 9, 10, 11]

while len(jie_ci) > 3:
    jie_ci=list(map(int,input('输入有误，请检查后重新输入：（节次 星期（可选） 周数（可选））').split()))
if len(jie_ci)==0:
    jie_ci=list(map(int,input('输入课程：（星期（可选）节次 周数（可选））').split()))
if len(jie_ci)==3:
    tele(hand(table,jie_ci))
if len(jie_ci)==2:
    jie_ci=jie_ci+[0]
    tele(hand(table,jie_ci))    
if len(jie_ci)==1:
    jie_ci=[0]+jie_ci
    tele(auto(table,jie_ci))

##schedule.every().day.at('07:55').do(auto,table,1)
##schedule.every().day.at('16:17:30').do(hand,table,[12,2,7])
##while True:
##    schedule.run_pending()
##    time.sleep(1)

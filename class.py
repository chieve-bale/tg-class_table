from bs4 import BeautifulSoup

file=open('C:\\Users\h2402\Desktop\课表.html',mode="r",encoding="utf-8")
ClassTab=file.read()
soup=BeautifulSoup(ClassTab, "html.parser")

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
            print(tag_id,'\n******************************************************')
            time=w*1000+c
            print(name)
            for i in div_tag.find('span',attrs={'title':'节/周'}).next_siblings:
                print(i.string)
                week=i.string
            for i in div_tag.find('span',attrs={'title':'上课地点'}).next_siblings:
                print(i.string)
                site=i.string
            for i in div_tag.find('span',attrs={'title':'教师'}).next_siblings:
                print(i.string)
                teacher=i.string
            for i in div_tag.find('span',attrs={'title':'学分'}).next_siblings:
                print(i.string)
                credit=i.string
            for i in div_tag.find('span',attrs={'title':'课程学时组成'}).next_siblings:
                print(i.string)
                period=i.string 
            table=table+[{'name':name,'week':week,'time':time,'site':site,'teacher':teacher,'credit':credit,'period':period}]

print(table)
file.close()

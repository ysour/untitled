# encoding:utf-8
import sys
from bs4 import BeautifulSoup
import urllib,urllib2
import threading
import os

GroupUrl ="https://www.douban.com/group/haixiuzu/"
reload(sys)
sys.setdefaultencoding('utf-8')



def getTopicList(url):
    while(True):
        startPage = int(input("起始页:"))
        endPage = int(input("结束页:"))
        if startPage<=0 or endPage<=0:
            print '输入非法'
        else:
            break
    for x in range(startPage-1, endPage-1):
        page = x * 25
        realurl = url +"discussion?start="+str(page)

        req = urllib2.Request(realurl)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
        req.add_header("GET", realurl)
        req.add_header("Host", "www.douban.com")
        req.add_header("Referer", "http://www.douban.com/")

        opener = urllib2.build_opener()
        html = opener.open(req).read()

        soup = BeautifulSoup(html,"html.parser")
        tdList = soup.find_all("td",class_='title')
        for i in tdList:
            title = i.a.get('title')
            if len(i.contents) > 1:
                if '晒' in title:
                    i_href = i.a.get('href')
                    getTopicContext(i_href)

def getTopicContext(topicUrl):
    req = urllib2.Request(topicUrl)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
    req.add_header("GET", topicUrl)
    req.add_header("Host", "www.douban.com")
    req.add_header("Referer", "http://www.douban.com/")
    opener = urllib2.build_opener();
    html = opener.open(req)

    soup = BeautifulSoup(html,"html.parser")
    divs = soup.find_all("div",class_='topic-figure cc')
    for div in divs:
        if len(div.contents) > 1:
            imgSrc = div.img.get('src')
            t = threading.Thread(target=saveImage,args=(imgSrc,))
            t.setDaemon(True)
            t.start()

def auto_down(url,filename):
    try:
        urllib.urlretrieve(url,filename)
        return filename
    except urllib.ContentTooShortError:
        print 'Network conditions is not good.Reloading.'
        return auto_down(url,filename)

def saveImage(imgUrl):
    fileName = imgUrl[imgUrl.rfind("/")+1:]
    if(os.path.isdir("img")==False):
        os.mkdir("img")
        print "不存在目录 新建中"
    path = "img/"+fileName
    print auto_down(imgUrl, path)



if __name__ == "__main__":
    print GroupUrl
    getTopicList(GroupUrl)

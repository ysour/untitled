# encoding:utf-8
import sys
from bs4 import BeautifulSoup
import time
import urllib,urllib2
import threading
import os
import PIL.Image as Image

MainUrl ="http://www.topit.me/user/2776009"

reload(sys)
reload(sys)
sys.setdefaultencoding('utf-8')
global count
count = 0
def getGoodPicture(imgpath):
    img = Image.open(imgpath)
    YCbCrimg = img.convert('YCbCr')
    w, h = YCbCrimg.size

    data = YCbCrimg.getdata()
    cnt = 0
    for i, ycbcr in enumerate(data):
        y, cb, cr = ycbcr
        if 97.5 <= cb <= 142.5 and 134 <= cr <= 176:
            cnt += 1
    if(cnt>w*h*0.3):
        global count
        count=count+1
        img.close()
        return True
    else:
        os.remove(imgpath)
        img.close()
        return False

def getTopicList(url):
    startPage = 1
    endPage = 2
    for x in range(startPage, endPage):
        realurl = url +"?p="+str(startPage)

        req = urllib2.Request(realurl)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
        req.add_header("GET", realurl)
        req.add_header("Host", "www.topit.me")
        req.add_header("Referer", realurl)

        opener = urllib2.build_opener()
        html = opener.open(req).read()


        soup = BeautifulSoup(html,"html.parser")
        tdList = soup.find_all("div",class_='t')
        c= 0;
        for i in tdList:
            href = i.a.img.get('src')
            if '.gif' not in href:
                c+=1
                print href,c
                #threading.Thread(target=saveImage, args=(href,)).start()
                saveImage(href)
                time.sleep(1)
            else:
                c+=1
                href = i.a.img.get("data-original")
                print href+"链接已修复",c
                #threading.Thread(target=saveImage, args=(href,)).start()
                saveImage(href)
                time.sleep(1)

def auto_down(url,filename):
    try:
        urllib.urlretrieve(url,filename)
        return filename
    except urllib.ContentTooShortError:
        return auto_down(url,filename)

def saveImage(imgUrl):
    fileName = imgUrl[imgUrl.rfind("/")+1:]
    if(os.path.isdir("img")==False):
        print "不存在目录 新建中"
        os.mkdir("img")
    path = "img/"+fileName
    print auto_down(imgUrl,path)
    try :
        print '%s' %(''if getGoodPicture(path)==True else 'not sexy ')
    except IOError:
        print "文件错误"
if __name__ == "__main__":
    print MainUrl
    getTopicList(MainUrl)

    print "共%d张" % (count)
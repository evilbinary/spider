#!/usr/bin/python
#coding=utf-8
#post by EvilBinary 小E
#Filename: get.py

import urllib,urllib2,cookielib,re,os
import fnmatch,sys,time,random
import time  
import thread
import threading
import hashlib 

cookie=cookielib.CookieJar()

def getUrlContent(url,action):
        try:
                opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)","Internet Explorer 7 (Windows Vista); Mozilla/4.0 ","Google Chrome 0.2.149.29 (Windows XP)","Opera 9.25 (Windows Vista)","Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)","Opera/8.00 (Windows NT 5.1; U; en)"]
                agent = random.choice(agents)   
                #agent=agents[4]
                print agent
                opener.addheaders=[('User-agent',agent)]
                urllib2.install_opener(opener)
                print "GET "+url+action
                req=urllib2.Request(url+action)
                u=urllib2.urlopen(req)
                content=u.read()
                return content
        except Exception,e:
		print 'Error'
		print e

def getImageUrl(content):
	#str='<img[\s\S]*src="(.*?)"'
	str='src="(.*?)"'
	reObj=re.compile(str)
	allMatch=reObj.findall(content)
	#print allMatch
	if allMatch:
		print "fount:",len(allMatch)
		return allMatch
	else:
		print "no fount image url"
		return ''

def downLoadImg(url,name):
        try:
                req=urllib2.Request(url)
                u=urllib2.urlopen(req)
                content=u.read()
                f = open(os.getcwd()+ '/'+name, "w+b")
                f.write(content)
                f.close()
        except Exception,e:
                print 'Error',e
class MyThread(threading.Thread):
        def __init__(self, threadname,imageUrl,imageName):  
                threading.Thread.__init__(self, name=threadname)
                self.imgUrl=imageUrl
                self.imgName=imageName
        def run(self):
                try:
                        downLoadImg(self.imgUrl,self.imgName)
                        time.sleep(1)  
                        print '%s is running......done.'%self.getName()
                except Exception,e:
                        print 'Error',e


if __name__ == "__main__":
        try:
                if len(sys.argv) < 2:
                        print "usage :", sys.argv[0], "<url>"
                        exit(1)
                else:
                        url= sys.argv[1]
                        content=getUrlContent(url,'')
                        #f = open(os.getcwd()+ '/ret.html', "w+b")
                        #f.write(content)
                        #f.close()
                        #print unicode(content,'utf-8','ignore').encode('gbk','ignore')
                        imgUrl=getImageUrl(content)
                        for url in imgUrl:
                                urlHash=hashlib.sha1(url).hexdigest()
                                imgName=url.split('/')[-1]
                                imgExt=url.split('.')[-1]
                                print  url,imgName,imgExt
                                
                                if imgExt=='jpg' or imgExt=='gif' or imgExt=='jpeg'  or imgExt=='png'  or imgExt=='jpeg':
                                        myThread=MyThread('evilbinary-'+imgName,url,'img/'+urlHash+'_'+imgName)
                                        myThread.start()
                                #print unicode(imgUrl,'utf-8','ignore').encode('gbk','ignore')
        except Exception,e:
		print 'Error',e

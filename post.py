#!/usr/bin/python
#coding=utf-8
#post by EvilBinary 小E 实现Discuz X 的post自动提交。
#Filename: post.py

import urllib,urllib2,cookielib,re,os
import fnmatch,sys,time,random

url ='http://bbs.xxxxxx.net/'
loginhash=''
sechash=''
formhash=''
fid='0'

cookie=cookielib.CookieJar()
def login(username,password):
	global sechash
	global formhash
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)","Internet Explorer 7 (Windows Vista); Mozilla/4.0 ","Google Chrome 0.2.149.29 (Windows XP)","Opera 9.25 (Windows Vista)","Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)","Opera/8.00 (Windows NT 5.1; U; en)"]
	agent = random.choice(agents)   
	#agent=agents[4]
	print agent
	#opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
	opener.addheaders=[('User-agent',agent)]
	urllib2.install_opener(opener)
	
	content = ""
	err_count = 0
	flage = True
	while flage:
		try:
			action='forum.php?mod=post&action=newthread&fid='+fid+'&infloat=yes&handlekey=newthread&inajax=1&ajaxtarget=fwin_content_newthread'
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content
			
			str='[\s\S]*<input\s*type="hidden"\s*name="formhash"\s*value="(.*?)"\s*\/>[\s\S]*'
			reObj=re.compile(str)
			allMatch=reObj.findall(content)
			formhash=allMatch[0]
			print "fromhash:"+formhash
			
			action='forum.php?mod=post&action=newthread&fid=2&infloat=yes&handlekey=newthread&inajax=1&ajaxtarget=fwin_content_newthread'
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content      
			loginhash=getLoginHash(content)
			print "loginhash:"+loginhash
			sechash=getSecHash(content)
			print "sechash:"+sechash

			action='member.php?mod=logging&action=login&handlekey=newthread&infloat=yes&inajax=yes&guestmessage=yes'
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content

			action='misc.php?mod=seccode&action=update&idhash='+sechash+'&inajax=1&ajaxtarget=seccode_'+sechash
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content

			imageUrl=getVerifyImageUrl(content)
			print "GET "+url+imageUrl
			while True:	
				req=urllib2.Request(url+imageUrl)
				req.add_header('Accept', '*/*')
				req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
				req.add_header('Connection', 'keep-alive')
				req.add_header('Origin', url)
				req.add_header('Referer', url+"forum.php")
				u=urllib2.urlopen(req)
				if not u.headers['Content-Type'].startswith('image'):  
					print "cant get verify image"
				else:
					print "GET Verify Image"
					content=u.read()
					#print os.getcwd()+ '/verify.png'
					f = open(os.getcwd()+ '/verify.png', "w+b")
					f.write(content)
					f.close()   
					seccodeverify = raw_input("input:")
					action='misc.php?mod=seccode&action=check&inajax=1&&idhash='+sechash+'&secverify='+seccodeverify
					print "GET "+url+action
					req=urllib2.Request(url+action)
					u=urllib2.urlopen(req)
					content=u.read()
					#print content
	
					if content.find('succeed')!=-1:
						#print "succeed "+content
						action="member.php?mod=logging&action=login&loginsubmit=yes&handlekey=newthread&loginhash="+loginhash+"&inajax=1"
						logindata=(('formhash',formhash), ('referer','http://hacking-linux.com/forum.php'), ('username',username), ('password',password) ,('questionid','0') ,('answer',''),('sechash',sechash), ('seccodeverify',seccodeverify) ,('loginsubmit','true'))
						print "POST "+url+action
						req=urllib2.Request(url+action,urllib.urlencode(logindata))
						req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
						#req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
						#req.add_header('Connection', 'keep-alive')
						req.add_header('Referer', url+"forum.php")
						u=urllib2.urlopen(req)
						content=u.read()
						flage=False
						#print unicode(content,'utf-8','ignore').encode('gbk','ignore')
						break
						print content
					else:
						print "verify faild"

		except urllib2.HTTPError, e:
			if err_count > 10:
				print "exit"
				exit(1)
			err_count += 1
			print e
			flage = True
			if e.getcode()== 403:
				print "Wait for 5 minutes..."
				time.sleep(5 * 60)

	#print content
	return content

def verify():
	return ''
def getLoginHash(content):
	str='<form method="post"[\s\S]*name="login"[\s\S]*action="member.php[\s\S]*loginhash=(.*?)">'
	reObj=re.compile(str)
	allMatch=reObj.findall(content)
	if allMatch:
		#print "fount"
		loginhash=allMatch[0]
		#print loginhash
		return loginhash
	else:
		print "no fount login hash"
		return ''
def getVerifyImageUrl(content):
	str='<img[\s\S]*src="(.*?)"'
	reObj=re.compile(str)
	allMatch=reObj.findall(content)
	if allMatch:
		#print "fount"
		imageUrl=allMatch[0]
		#print imageUrl
		return imageUrl
	else:
		print "no fount image url"
		return ''

def getSecHash(content):
	str='<input\s*name="sechash"\s*type="hidden"\s*value="(.*?)"\s*\/>'
	reObj=re.compile(str)
	allMatch=reObj.findall(content)
	if allMatch:
		#print "fount"
		secHash=allMatch[0]
		#print secHash
		return secHash
	else:
		print "no fount sechash url"
		return ''

def getAuth(content):
	str='[\s\S]*auth=(.*?)&referer[\s\S]*'
	reObj=re.compile(str)
	allMatch=reObj.findall(content)
	if allMatch:
		#print "fount"
		auth=allMatch[0]
		#print secHash
		return auth
	else:
		print "no fount auth"
		return ''
def getVerifyInfo(content):
	#print content
	#print "getVerifyInfo"  
	m = re.match("[\s\S]*showWindow\(\'(.*)\',\s*\'(.*?)\'\)[\s\S]*",content) 
	if m:
		#print m.group(2)
		return m.group(2)
	else:
		print "verify url no found"
		return ''

def getResultInfo(content):
	p = re.compile('<div\s*id="messagetext"\s*class="alert_error"\s*>\s*<p>(.*?)\s*<script\s*')
	m = p.findall(content)
	if len(m) > 0:
		for i in m:
			print  i.replace('</p>','').decode('gbk','ignore')  
		return m[0].replace('</p>','')
	else:
		print "result info no found"
		return ''
def post(fid,title,contents):
        global sechash
        global formhash
        #print "sechash:"+sechash
	content = ""
	err_count = 0
	flage = True
	while flage:
		try:
			action='forum.php'
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content
						            
			str='[\s\S]*<input\s*type="hidden"\s*name="formhash"\s*value="(.*?)"\s*\/>[\s\S]*'
			reObj=re.compile(str)
			allMatch=reObj.findall(content)
			formhash=allMatch[0]
			print "fromhash:"+formhash
			#print content
						    
			#print "sechash:"+sechash
			action='misc.php?mod=seccode&action=update&idhash='+sechash+'&inajax=1&ajaxtarget=seccode_'+sechash
			print "GET "+url+action
			req=urllib2.Request(url+action)
			u=urllib2.urlopen(req)
			content=u.read()
			#print content
			          
			imageUrl=getVerifyImageUrl(content)
			print "GET "+url+imageUrl
			while True:				
				req=urllib2.Request(url+imageUrl)
				req.add_header('Accept', '*/*')
				req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
				req.add_header('Connection', 'keep-alive')
				req.add_header('Origin', url)
				req.add_header('Referer', url+"forum.php")
				u=urllib2.urlopen(req)
				if not u.headers['Content-Type'].startswith('image'):  
					print "cant get verify image"
				else:
					print "GET Verify Image"
					content=u.read()
					#print os.getcwd()+ '/verify.png'
					f = open(os.getcwd()+ '/verify.png', "w+b")
					f.write(content)
					f.close()   
					seccodeverify = raw_input("input:")
		                           
					action='misc.php?mod=seccode&action=check&inajax=1&&idhash='+sechash+'&secverify='+seccodeverify
					print "GET "+url+action
					req=urllib2.Request(url+action)
					u=urllib2.urlopen(req)
					content=u.read()
					print content
					if content.find('succeed')!=-1:
						action="forum.php?mod=post&action=newthread&fid="+fid+"&topicsubmit=yes&infloat=yes&handlekey=fastnewpost&inajax=1"
						postdata=(('subject',title), ('message',contents),('sechash',sechash) ,('seccodeverify',seccodeverify) ,('formhash',formhash) ,('usesig','1') ,('posttime','1370620456'))
						print "POST "+url+action
						#print postdata
						req=urllib2.Request(url+action,urllib.urlencode(postdata))
						req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
						req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
						#req.add_header('Connection', 'keep-alive')
						req.add_header('Referer', url+"forum-"+fid+"-1.html")
						req.add_header('Origin', url)
						u=urllib2.urlopen(req)
						content=u.read()
						#print unicode(content,'utf-8','ignore').encode('gbk','ignore')
						print content
						flage=False
						break
					else:
						print "verify code fail"

		except urllib2.HTTPError, e:
			if err_count > 10:
				exit(1)
			err_count += 1
			print e
			flage = True
			if e.getcode() == 403:
				print "Wait for 5 minutes..."
				time.sleep(5 * 60)
	

def postAllFile(path,fid):
	if(path==''):
		path='./'
		print 'null'
	else:
		for fileName in os.listdir (path):
			if fnmatch.fnmatch ( fileName, '*.txt' ):
				initsize=900
				print 'Posting... '+fileName
				f=open(path+fileName,"r")
				contents=f.read()
				fileName=fileName.replace('.txt','')
				count=0
				totallen=len(contents)
				oder=0
				while count<= totallen:
					if count==0:
						fileName=unicode(fileName,'utf-8','ignore').encode('gbk','ignore')
					else:
						fileName=unicode(fileName+'继'+str(oder),'utf-8','ignore').encode('gbk','ignore')    
					c= unicode(contents[count:count+initsize],'utf-8','ignore').encode('gbk','ignore')
					post(fid,fileName,c)
					#time.sleep(20)
					#print fileName
					#print c
					count+=initsize
					oder+=1
				f.close()
				

if __name__ == "__main__":
	fid='0'
	if len(sys.argv) < 2:
		print "usage :", sys.argv[0], "<username> <password> <url> <fid> "
		exit(1)
	else:
		try:
			username = sys.argv[1]
			password=sys.argv[2]
			if len(sys.argv) >3:
				url=sys.argv[3]
			if len(sys.argv)>4:
				fid=sys.argv[4]
			#print username+' '+password+' '+url+' '+fid
			login(username,password)
			postAllFile('./',fid)
		except Exception,e:
			print 'Error'
			print e


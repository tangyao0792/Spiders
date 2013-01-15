#!/usr/bin/python
# coding=utf-8

'''Downloader for acm.hdu.edu.cn solutions.
====================================================================
#   Author:	    	TangYao - tangyao0792.github.com
#   Email:			tangyao0792@gmail.com
#   Version:		1.0
#   Last change:	2012.01.15
====================================================================
#
'''

import sys
import urllib
import urllib2
import cookielib
import HTMLParser
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


def initialCookie():
    #set cookie
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)


def login(userid, password):
    ''' input username and pwd, return the html string after login'''
    xn = {}
    xn['username'] = userid
    xn['userpass'] = password
    xn['login'] = 'Sign+In'

    info = urllib.urlencode(xn)
    request = urllib2.Request('http://acm.hdu.edu.cn/userloginex.php?'
                              'action=login&cid=0&notice=0', info)
    response = urllib2.urlopen(request)
    html = response.read()
    if not html.find('wrong') > 0:
        print 'login successfully'
        return True
    else:
        print 'login unsucessfully'
    return False


html_parser = HTMLParser.HTMLParser()


def saveSource(runid, problemid):
    f = open('hdoj/hdu' + str(problemid) + '_' + str(runid) + '.cpp', 'w+')
    oldStdout = sys.stdout
    sys.stdout = f
    url = 'http://acm.hdu.edu.cn/viewcode.php?rid=%s' % runid
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html)
    pre = soup.find('textarea').getText().decode('utf-8')
    print '/*'
    print ' *   Author: Tangyao'
    print ' *   Email:  tangyao0792@gmail.com'
    print ' *   tangyao0792.github.com'
    print ' */'
    print html_parser.unescape(pre)
    sys.stdout = oldStdout
    f.close()


def download(userid):
    url = 'http://acm.hdu.edu.cn/status.php?first=&pid=&user=%s&lang=0&status=5' \
          % str(userid)
    #output redirection
    while True:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html)
        tds = soup.findAll('td', {'height': '22px'})
        
        runid = 0
        problem_id = 0

        for td in tds:
            for i in range(0, 9):
                if i == 0:
                    runid = int(td.getText())
                elif i == 3:
                    problem_id = td.getText()
                td = td.findNextSibling()
            print runid,'   ',problem_id
            saveSource(runid, problem_id)

        if runid == 0:
            break
        url = 'http://acm.hdu.edu.cn/status.php?first=%s&user=%s&pid=&lang=&status=5#status' \
              % (str(runid - 1) , userid)

if __name__ == '__main__':
    initialCookie()
    userid = raw_input('userid: ')
    password = raw_input('password: ')
    if login(userid, password):
        download(userid)

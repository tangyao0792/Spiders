#!/usr/bin/python
# coding=gbk

'''Downloader for poj.org solutions.
====================================================================
#   Author:	    	TangYao - tangyao0792.github.com
#   Email:			tangyao0792@gmail.com
#   Version:		1.0
#   Last change:	2012.01.12
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
    xn['user_id1'] = userid
    xn['password1'] = password
    xn['B1'] = 'login'
    xn['url'] = '.'
    info = urllib.urlencode(xn)
    request = urllib2.Request('http://poj.org/login?', info)
    response = urllib2.urlopen(request)
    html = response.read()
    if html.find('loginlog') > 0:
        print 'login successfully'
        return True
    else:
        print 'login unsucessfully'
    return False


def parseTR(tr):
    td = tr.td
    runid = td.getText()
    problemId = td.findNextSibling().findNextSibling().getText()
    #print runid, '   ', problemId
    return runid, problemId

html_parser = HTMLParser.HTMLParser()


def saveSource(runid, problemid):
    f = open('poj/poj' + str(problemid) + '_' + str(runid) + '.cpp', 'w+')
    oldStdout = sys.stdout
    sys.stdout = f
    url = 'http://poj.org/showsource?solution_id=%s' % runid
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html)
    pre = soup.find('pre').getText().decode('utf-8')
    print '/*'
    print ' *   Author: Tangyao'
    print ' *   Email:  tangyao0792@gmail.com'
    print ' *   tangyao0792.github.com'
    print ' */'
    print html_parser.unescape(pre)
    sys.stdout = oldStdout
    f.close()


def download(userid):
    url = 'http://poj.org/status?problem_id=&user_id=%s&result=0' \
          % str(userid)
    #output redirection
    while True:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html)
        tag = soup.find('table', {'class': 'a'})
        tr = tag.tr
        runid = 0
        problem_id = 0
        while True:
            tr = tr.findNextSibling()
            if not tr:
                break
            else:
                print runid, '   ', problem_id
                runid, problem_id = parseTR(tr)
                saveSource(runid, problem_id)
        if runid == 0:
            break
        url = 'http://poj.org/status?problem_id=&user_id=%s&result=0&top=%s'\
              % (str(userid), str(runid))

if __name__ == '__main__':
    initialCookie()
    userid = raw_input('userid: ')
    password = raw_input('password: ')
    login(userid, password)
    download(userid)

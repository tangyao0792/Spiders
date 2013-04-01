#!/usr/bin/python
# coding=utf-8

'''
#=============================================================================
#     FileName: neugpa.py
#         Desc: 
#       Author: Tang Yao
#        Email: tangyao0792@gmail.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2013-01-23 22:14:17
#      History:
#=============================================================================
'''


import urllib2
import urllib
import cookielib
import HTMLParser

html_parser = HTMLParser.HTMLParser()
    
def initialCookie():
    #set cookie
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)


def login(userid, password):
    ''' input username and pwd, return the html string after login'''
    xn = {}
    xn['WebUserNO'] = userid
    xn['Password'] = password

    info = urllib.urlencode(xn)
    request = urllib2.Request('http://202.118.31.197/ACTIONLOGON.APPPROCESS', info)
    response = urllib2.urlopen(request)
    request = urllib2.Request('http://202.118.31.197/ACTIONQUERYSTUDENTSCORE.APPPROCESS')
    response = urllib2.urlopen(request)
    html = response.read()
    return html


def selectYear(YearTermNO):
    ''' select the year'''
    xn = {}
    xn['YearTermNO'] = str(YearTermNO)
    info = urllib.urlencode(xn)
    request = urllib2.Request('http://202.118.31.197/ACTIONQUERYSTUDENTSCORE.APPPROCESS', info)
    response = urllib2.urlopen(request)
    return response.read()


def parseHTML(html):
    '''parse the html file to lesson and score
    '''
    term = []
    first = 0
    cnt = 0
    while True:
        html = html[first+1:]
        first = html.find('row')
        tmp = html[first:]
        second = tmp.find('</tr>')
        if first == -1:
            break
        content = html[first : first + second]
        left = content.find('nbsp') + 5
        right = content[left:].find('<')
        lesson = content[left : left+right]
        lines = content.split('</td>')
        tmp = lines[len(lines)-2]
        left = tmp.find('p>')
        score = tmp[left + 2:]
        cnt = cnt + 1
        term.append((lesson, score))
    return term


if __name__ == '__main__':
    initialCookie()
    html = login(20101234, 'your password')
    html = html.decode('gbk')
#
    html = selectYear(14)
    term = parseHTML(html)
    for tup in term:
        print tup[0], tup[1]

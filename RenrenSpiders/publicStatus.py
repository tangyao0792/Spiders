#!/usr/bin/python
# coding=utf-8

'''A simple script for public a status to renren.com.
====================================================================
#   Author:		TangYao - tangyao0792.github.com
#   Email:			tangyao0792@gmail.com
#   Version:		1.0
#   Last change:	2012.01.12
====================================================================
#The key point to public a status without renren's api is getting
the hidden infomation in the form.
'''

from time import sleep
import urllib
import urllib2
import cookielib
import string


def initialSender():
    #set cookie
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)


def login():
    ''' input email and pwd, return the html string after login'''
    xn = {}
    xn['email'] = raw_input('email:	')
    xn['password'] = raw_input('password:	')
    info = urllib.urlencode(xn)
    request = urllib2.Request('http://www.renren.com/PLogin.do', info)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

digits = string.digits


def getHiddenNumber(key):
    '''get the first number after str key'''
    position = html.find(key) + len(key)
    while html[position] not in digits:
        position = position + 1
    number = 0
    while html[position] in digits:
        number = number * 10 + int(html[position])
        position = position + 1
    return number


def getHiddenInfo(html):
    '''some hidden key and values not in the form, but need to be sent'''
    hiddenInfo = {}
    hiddenInfo['hostid'] = str(getHiddenNumber('hostid'))
    hiddenInfo['requestToken'] = str(getHiddenNumber('get_check'))
    hiddenInfo['channel'] = 'renren'
    # get _rtk, _rtk is a string
    left = html.find('get_check_x') + len('get_check_x')
    while True:
        if html[left] == "'":
            break
        left = left + 1
    right = left + 1
    while True:
        if html[right] == "'":
            break
        right = right + 1
    hiddenInfo['_rtk'] = html[left + 1: right]
    print hiddenInfo
    return hiddenInfo


def sendStatus(status):
    status = urllib.urlencode(status)
    req = urllib2.Request('http://shell.renren.com/466114025/status', status)
    resp = urllib2.urlopen(req)
    html = resp.read()

if __name__ == '__main__':
    initialSender()
    html = login()
    status = getHiddenInfo(html)
    content = raw_input('status:	')
    count = 0
    # loops :)
    while True:
        status['content'] = content + '第' + str(count) + '次'
        sendStatus(status)
        count = count + 1
        print status

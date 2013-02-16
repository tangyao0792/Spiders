#!/usr/bin/python
#coding=utf-8
'''
#=============================================================================
#     FileName: TiebaSpider.py
#         Desc: Get info about a tieba.
#       Author: Tang Yao
#        Email: tangyao0792@gmail.com
#     HomePage:
#      Version: 0.0.1
#   LastChange: 2013-02-14 15:55:51
#      History:
#=============================================================================
'''

import urllib
import urllib2
from chardet import detect

count_html = 0

# i'am a browser
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

# proxy

#proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0.1:8088'})
#opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
#urllib2.install_opener(opener)

def get_html_by_url(url):
    print '***********      ', url,
    global count_html, headers
    count_html += 1
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    print '     ok..'
    return response.read()

def get_dir(name):
    first_dir = ''
    second_dir = ''
    url = 'http://tieba.baidu.com/f?ie=utf-8&kw=' + name
    html = ''
    html = get_html_by_url(url)
    l = html.find('/f/fdir?fd=')
    html = html[l : ]
    r = html.find('"')
    # url to the dir
    url = 'http://tieba.baidu.com' + html[:r]

    html = get_html_by_url(url)
    l = html.find('<title>')
    r = html.find('</title>')
    html = html[l + 7 : r]
    dirs = html.split('_')
    if len(dirs) > 2:
        first_dir = dirs[1][ : -6]
    second_dir = dirs[0]
    first_dir = first_dir.decode('gbk').encode('utf-8')
    second_dir = second_dir.decode('gbk').encode('utf-8')
    return first_dir, second_dir


def get_dir_and_links(name):
    first_dir = ''
    second_dir = ''
    url = 'http://tieba.baidu.com/f?ie=utf-8&kw=' + name
    html = ''
    html = get_html_by_url(url)
    temp_html = html
    l = html.find('/f/fdir?fd=')
    html = html[l : ]
    r = html.find('"')
    # url to the dir
    url = 'http://tieba.baidu.com' + html[:r]

    # links
    links = []
    html = temp_html
    l = html.find('zyq_mod_friend_items')
    html = html[l : ]
    r = html.find('</ul>')
    html = html[ : r]
    while True:
        l = html.find('j_mod_item')
        if l == -1: break
        html = html[l : ]
        l = html.find('>') + 1
        r = html.find('<')
        name = html[l : r]
        html = html[r :]
        name = name.decode('gbk').encode('utf-8')
        links.append(name)
    # links ends

    # get dirs
    html = get_html_by_url(url)
    l = html.find('<title>')
    r = html.find('</title>')
    html = html[l + 7 : r]
    dirs = html.split('_')
    if len(dirs) > 2:
        first_dir = dirs[1][ : -6]
    second_dir = dirs[0]
    first_dir = first_dir.decode('gbk').encode('utf-8')
    second_dir = second_dir.decode('gbk').encode('utf-8')
    return first_dir, second_dir, links


def get_links(name):
    '''return the friendly links of a tieba'''
    links = []
    url = 'http://tieba.baidu.com/f?ie=utf-8&kw=' + name
    html = get_html_by_url(url)
    l = html.find('zyq_mod_friend_items')
    html = html[l : ]
    r = html.find('</ul>')
    html = html[ : r]
    while True:
        l = html.find('j_mod_item')
        if l == -1: break
        html = html[l : ]
        l = html.find('>') + 1
        r = html.find('<')
        name = html[l : r]
        html = html[r :]
        name = name.decode('gbk').encode('utf-8')
        links.append(name)
    return links

def main():
    get_links('五月天')
    get_links('c++')
    get_links('足球')



if __name__ == '__main__':
    main()

#!/usr/bin/python
#coding=utf-8
'''
#=============================================================================
#     FileName: Walker.py
#         Desc: 
#       Author: Tang Yao
#        Email: tangyao0792@gmail.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2013-02-14 16:26:30
#      History:
#=============================================================================
'''

from TiebaSpider import count_html
from TiebaSpider import get_dir_and_links
from copy import deepcopy
from Queue import PriorityQueue
from time import time 


class Node:
    def __init__(self):
        self.name = ''
        self.first_dir = ''
        self.second_dir = ''
        self.path = []
        self.weight = 0.0
        self.links = []

    def __cmp__(self, node):
        if isinstance(node, Node):
            return cmp(self.weight, node.weight)
        elif isinstance(node, int):
            return cmp(self.weight, node)

def Make_node(name, target_node=None, path=[]):
    '''make a Node of name, with the target_node,
       path is the path from started tieba to the last tieba before name'''
    print 'making node for', name
    node = Node()
    node.name = name
    node.first_dir, node.second_dir, node.links = get_dir_and_links(name)
    if len(path) > 0:
        node.path = deepcopy(path)
    node.path.append(name)

    if not target_node is None:
        # calulate the weight
        if node.first_dir == target_node.first_dir:
            node.weight -= 1000
        if node.second_dir == target_node.second_dir:
            node.weight -= 10000
        node.weight /= float(len(node.path))
    print 'ok...'
    print ''
    return node


def astar(start, target):
    visit = []
    target_node = Make_node(target)
    start_node = Make_node(start, target_node)
    que = PriorityQueue()
    que.put(start_node)
    while que.empty() is False:
        current_node = que.get()
        print 'current tieba:', current_node.name
        print 'weigth:       ', current_node.weight
        for l in current_node.links:
            # found
            if l == target:
                current_node.path.append(l)
                return current_node.path
            # has handled
            if l in visit:
                continue
            visit.append(l)
            next_node = Make_node(l, target_node, current_node.path)
            que.put(next_node)
    return None

def main():
    start = raw_input('start:   ')
    target = raw_input('target:   ')
    now = time()
    path = astar(start, target)
    during = time() - now
    if not path is None:
        print '*************************************************************'
        print '->'.join(path)
    else:
        print'*************no way**********'
    print 'number of pages:    ', count_html
    print 'cost of time:       ', during


if __name__ == '__main__':
    main()

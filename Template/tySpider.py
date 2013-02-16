#coding=utf-8
'''
#=============================================================================
#     FileName: tySpider.py
#         Desc: 
#       Author: Tang Yao
#        Email: tangyao0792@gmail.com
#     HomePage: 
#      Version: 0.0.1
#   LastChange: 2013-02-16 15:06:53
#      History:
#=============================================================================
'''

from threading import Thread
from Queue import Queue
from time import sleep
import traceback

class work_thread(Thread):
    def __init__(self, work_func, number, queue, rest_time=0):
        Thread.__init__(self)
        self.number = number
        self.work_func = work_func
        self.queue = queue                      # shallow copy
        self.rest_time = rest_time

    def run(self):
        try:
            while self.queue.empty() is False:
                arg, karg = self.queue.get()       # Queue in python is safe in multi threads
                self.work_func(*arg, **karg)    # work
                self.queue.task_done()
                if self.rest_time != 0:
                    sleep(self.rest_time)
        except Exception as e:
            print e
            print traceback.format_exc()
        print 'thread%s is over' % str(self.number)

       

class tySpider:
    def __init__(self, thread_num, work_func, rest_time=0, maxsize_queue=0):
        self.queue = Queue(maxsize_queue)   # work queue, params in it
        self.thread_num = thread_num        # max number of threads
        self.rest_time = rest_time          # when a task done, sleep such seconds
        self.work_func = work_func          # the function to be called
                                            # this func must be safe in multi threads
        self.my_thread = []

    def run(self):
        '''
            before call this function, put params into queue
        '''
        for i in range(self.thread_num):
            self.my_thread.append(work_thread(self.work_func, i, self.queue, rest_time=self.rest_time))
            self.my_thread[i].start()

        for i in range(self.thread_num):
            self.my_thread[i].join()
        print 'all task done'

#******************* debug ******************
def my_func(x):
    print x

def main():
    my_spider = tySpider(5, my_func, rest_time=1)
    for i in range(100):
        my_spider.queue.put(([i], {}))
    my_spider.run()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# coding: utf-8

import sys
import Queue
import traceback
import threading


class WorkerThread(threading.Thread):

    """
    WorkerThread
    """

    def __init__(self, working_queue, result_queue, error_queue, timeout):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.timeout = timeout
        self.working_queue = working_queue
        self.result_queue = result_queue
        self.error_queue = error_queue
        self.timeout = timeout
        self.start()

    def run(self):
        """
        执行操作
        """
        while True:
            command, callable, args, kwds = self.working_queue.get(block=True)
            if command == "stop":
                break
            try:
                if command != "process":
                    raise ThreadPoolManagerError
            except Exception:
                print("WorkerThread", sys.exc_info())
                self._report_error()
            else:
                ret = callable(*args, **kwds)
                self.result_queue.put(ret)

    def _report_error(self):
        """
        记录错误信息
        """
        self.error_queue.put(sys.exc_info()[:2])

    def dismiss(self):
        """
        设置stop
        """
        command = "stop"
        self.working_queue.put((command, None, None, None))


class ThreadPoolManager(object):

    """
    ThreadPoolManager
    """

    def __init__(self, size, timeout=30):
        super(ThreadPoolManager, self).__init__()
        self.size = size
        self.timeout = timeout
        self.working_queue = Queue.Queue(100)
        self.result_queue = Queue.Queue(100)
        self.error_queue = Queue.Queue(100)
        self.workers = {}
        self._init_thread_pool()

    def _init_thread_pool(self):
        """
        线程池初始化
        """
        if 0 < self.size <= 200:
            num = self.size
        else:
            num = 20
        for x in range(num):
            worker = WorkerThread(
                self.working_queue,
                self.result_queue,
                self.error_queue,
                self.timeout)
            self.workers[x] = worker
        print("thread_pool normal loading.")

    def _get_result(self, queue):
        """
        队列中获取数据
        """
        try:
            while True:
                yield queue.get_nowait()
        except Queue.Empty:
            raise StopIteration

    def add_task(self, callable, *args, **kwds):
        """
        添加任务
        """
        command = "process"
        self.working_queue.put((command, callable, args, kwds))

    def get_result(self):
        """
        获取结果
        """
        ret = []
        for x in self._get_result(self.result_queue):
            ret.append(x)
        return ret

    def get_error(self):
        """
        获取错误
        """
        for t, v in self._get_result(self.error_queue):
            print t, v

    def wait_join(self):
        for x in self.workers:
            self.workers[x].join(self.timeout)

    def destroy(self):
        """
        线程池销毁
        """
        for x in self.workers:
            self.workers[x].dismiss()
        for x in self.workers:
            self.workers[x].join()
        del self.workers


class ThreadPoolManagerError(Exception):

    """
    docstring for ThreadPoolManagerError
    """
    pass


def test(id):
    print "OK"


def main():
    tpm = ThreadPoolManager(20)
    for id in range(40):
        tpm.add_task(test, id)
    tpm.destroy()
    tpm.get_error()

if __name__ == '__main__':
    main()

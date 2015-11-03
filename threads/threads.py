#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################

import os
import sys
import traceback
import threading
import logging
import urllib2
import socket

from modules.md5 import get_md5_value
from modules.debug import debug

logger = logging.getLogger("spider.threads")


class WorkerThread(threading.Thread):

    """
    WorkerThread
    """

    def __init__(self, conf, url):
        threading.Thread.__init__(self)
        self.conf = conf
        self.url = url

    def run(self):
        """
        执行操作
        """
        logger.info("WorkerThread normal loading.")
        while True:
            if self.conf.event.isSet():
                break
            try:
                logger.info("WorkerThread:" + str(self.url))
                send_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Connection': 'keep-alive'}
                socket.setdefaulttimeout(30)
                logger.info("WorkerThread:" + str(self.url))
                req = urllib2.Request(self.url, headers=send_headers)
                res = urllib2.urlopen(req)
                html = res.read()
                s = html.decode(
                    'utf-8',
                    'replace').encode(
                    sys.getfilesystemencoding())
                #fu = urllib.urlopen(self.url)
                #s = fu.read()
            except Exception:
                self.conf.mutex.acquire()
                self.conf.url_success.append(self.url)
                self.conf.url_failed.append(self.url)
                self.conf.mutex.release()
                logging.info("WorkerThread Error")
                return "download webpage false."
            else:
                p = get_md5_value(s)
                if p in self.conf.page_set:
                    return "webpage has existed."
                else:
                    m = get_md5_value(self.url)
                    path = os.getcwd() + '/save/' + m + '.txt'
                    with open(path, "w") as fd:
                        fd.write(s)
                    self.conf.mutex.acquire()
                    self.conf.url_success.append(self.url)
                    self.conf.url_pages.append(s)
                    self.conf.url_map[self.url] = m
                    self.conf.page_set.append(p)
                    self.conf.mutex.release()
                    return "download webpage ok."


class WorkerThreadError(Exception):

    """
    docstring for WorkerThreadError
    """
    pass

if __name__ == '__main__':
    pass

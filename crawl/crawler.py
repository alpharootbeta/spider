#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################

import os
import sys
import threading
import logging

from crawl.url import get_urls
from threads.threads import WorkerThread
from modules.debug import debug

logger = logging.getLogger("spider.crawler")


class CrawlerConf(object):

    """
    docstring for CrawlerConf
    """

    def __init__(self, opt, conf):
        super(CrawlerConf, self).__init__()
        self.opt = opt
        self.conf = conf

    def crawler(self):
        """
        广度搜索入口
        """
        logger.info("crawler normal loading.")
        if self.opt.dbg:
            debug("crawler normal loading.")
        self.conf.url_current.append(self.opt.url)
        if self.opt.dbg:
            debug("root url", self.conf.url_current)
        try:
            depth = 1
            while depth <= self.opt.deep and len(self.conf.url_current) and \
                    self.conf.url_count < self.opt.pages:
                if self.opt.dbg:
                    debug("current depth", depth)
                logger.info("current depth : " + str(depth))
                depth = depth + 1
                self._crawler_download_url()
                self._crawler_update_url()
            if self.opt.dbg:
                debug("crawler normal quit.")
        except Exception:
            if self.opt.dbg:
                debug("crawler abnormal quit.")
                debug("crawler", sys.exc_info())
            raise CrawlerConfError

    def _crawler_download_url(self):
        """
        开始当前url列表
        """
        logger.info("crawler_download_url normal loading.")
        i = 0
        while i < len(self.conf.url_current):
            j = 0
            while i + j < len(self.conf.url_current) and j < self.opt.thread_number and \
                    self.conf.url_count <= self.opt.pages:
                self.conf.url_count += 1
                work_thread = WorkerThread(
                    self.conf,
                    self.conf.url_current[i + j])
                self.conf.thread_pool.append(work_thread)
                work_thread.start()
                j += 1
            i += j
            for x in self.conf.thread_pool:
                x.join(30)
            self.conf.thread_pool = []
            if self.conf.url_count > self.opt.pages:
                break
        self.conf.url_current = []
        logger.info("crawler_download_url normal quit.")

    def _crawler_update_url(self):
        """
        更新当前下载url列表
        """
        logger.info("crawler_update_url normal loading.")
        if self.opt.dbg:
            debug("crawler_update_url normal loading.")
            debug("url_pages", self.conf.url_pages)
        url_new = []
        for s in self.conf.url_pages:
            url_new += get_urls(s)
        self.conf.url_current = list(set(url_new) -
                                     set(self.conf.url_success) -
                                     set(self.conf.url_failed))
        if self.opt.dbg:
            debug("url_current", self.conf.url_current)
        logger.info("crawler_update_url normal quit.")


class CrawlerConfError(Exception):

    """
    docstring for CrawlerConfError
    """
    pass

if __name__ == "__main__":
    pass

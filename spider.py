#!/usr/bin/env python
# coding: utf-8

import os
import sys
import Queue
import datetime
import threading
import logging
import logging.config
from optparse import OptionParser

from crawl.crawler import *
from modules.serialize import *
from modules.debug import debug


class SpiderOpt(object):

    """
    Spider Options
    """

    def __init__(self):
        super(SpiderOpt, self).__init__()
        self.url = None
        self.deep = 0
        self.thread_number = 0
        self.pages = 0
        self.version = None
        self.dbg = None


class SpiderConf(object):

    """
    Spider Configure Information
    """

    def __init__(self):
        super(SpiderConf, self).__init__()
        self.mutex = threading.Lock()
        self.url_pages = []
        self.url_success = []
        self.url_failed = []
        self.url_current = []
        self.url_map = {}
        self.url_count = 0
        self.url_file = os.getcwd() + '/save/' + "spider.cpickle"
        self.page_set = []
        self.thread_pool = []
        self.event = threading.Event()
        self.time_cost = 0


def spider_conf(opt, conf):
    """
    程序初始配置
    """
    s1 = datetime.datetime.now()
    d1 = s1.strftime("%Y-%m-%d %H:%M:%S")
    if opt.dbg:
        debug("spider_conf normal loading.")
        debug("spider start time", d1)
    logger.info("spider_conf normal loading")
    try:
        crl = CrawlerConf(opt, conf)
        crl.crawler()
    except CrawlerConfError:
        logger.debug("CrawlerConfError")
        debug("CrawlerConfError", sys.exc_info())
    except Exception:
        logger.debug("spider_conf Exception")
        debug("spider_conf", sys.exc_info())
    s2 = datetime.datetime.now()
    d2 = s2.strftime("%Y-%m-%d %H:%M:%S")
    if opt.dbg:
        debug("spider_conf normal quit.")
        debug("spider end time", d2)
    d = s2 - s1
    conf.time_cost = d.seconds
    logger.info("spider_conf normal finish.")


def spider_stop(conf):
    """
    程序终止
    """
    if opt.dbg:
        debug("spider_stop normal loading.")
        #debug("url_map", conf.url_map)
    try:
        if conf.url_map:
            serialize_object(conf.url_file, conf.url_map)
    except SerializeError:
        logger.debug("SerializeError")
        debug("SerializeError", sys.exc_info())
    conf.event.set()
    for x in conf.thread_pool:
        if x.isAlive():
            x.join(30)
    if opt.dbg:
        debug("spider_stop normal quit.")
    logger.info("spider_stop normal finish.")


def spider_usage(opt):
    """
    生成选项帮助信息
    """
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option(
        '-u',
        action='store',
        type='string',
        dest='url',
        default='http://www.jxnu.edu.cn/',
        help='url address')
    parser.add_option(
        '-d',
        action='store',
        type='int',
        dest='deep',
        default=2,
        help='search deep')
    parser.add_option(
        '-v',
        action='store_true',
        dest='version',
        help='show version information')
    parser.add_option(
        '-p',
        action='store',
        type='int',
        dest='pages',
        default=1000,
        help='pages')
    parser.add_option(
        '--thread',
        action='store',
        type='int',
        dest='number',
        default=20,
        help='thread number')
    parser.add_option(
        '--debug',
        action='store_true',
        dest='debug',
        default=False,
        help='debug mode')
    (options, args) = parser.parse_args()
    if options.url:
        opt.url = options.url
    if options.deep:
        opt.deep = options.deep
    if options.version:
        opt.version = options.version
    if options.pages:
        opt.pages = options.pages
    if options.number:
        opt.thread_number = options.number
    if options.debug:
        opt.dbg = options.debug


def spider_env():
    """
    环境配置
    """
    try:
        logdir = os.getcwd() + '/log/'
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        filedir = os.getcwd() + '/save/'
        if not os.path.exists(filedir):
            os.mkdir(filedir)
    except Exception:
        print sys.exc_info()
        exit()


def spider_result():
    """
    结果统计
    """
    res = "Spider Result: \n\nRoot URL: {0}\nMax Depth: {1}\n" + \
        "Total Pages: {2}\nURL Success: {3}\nURL Failed: {4}\nTime Cost: {5}s"
    print res.format(opt.url, opt.deep, conf.url_count, len(conf.url_success), len(conf.url_failed), conf.time_cost)


def spider_version(opt):
    """
    显示版本信息
    """
    if opt.version:
        print 'spider : 1.0.1'
        exit()

"""
global operation
"""
opt = SpiderOpt()
conf = SpiderConf()
spider_env()
logging.config.fileConfig("./conf/logging.conf")
logger = logging.getLogger("spider")


def spider():
    """
    爬虫程序入口
    """
    global opt, conf
    print("spider normal loading. ")
    spider_usage(opt)
    spider_version(opt)
    if opt.dbg:
        debug("spider entry debug mode.")
        debug("spider normal loading.")
        debug("options", opt.url, opt.deep, opt.pages, opt.thread_number)
    try:
        spider_conf(opt, conf)
        spider_stop(conf)
        if opt.dbg:
            debug("spider normal quit.")
        spider_result()
    except Exception:
        debug("Spider Exception", sys.exc_info())

    logger.info("spider normal stop.")

if __name__ == "__main__":
    spider()

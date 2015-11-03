#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################

import os
import time
from modules.serialize import *
from modules.debug import debug

FILEPATH = './save/spider.cpickle'


def load_file():
    """
    加载文件
    """
    urlmap = {}
    try:
        urlmap = unserialize_object(FILEPATH)
        return urlmap
    except SerializeError:
        debug("search", sys.exc_info())

    return None


def search():
    """
    根据输入的url查找相应的文件
    """
    opt = ['q', 'Q', 'quit', 'Quit']
    urlmap = {}
    urlmap = load_file()
    if not urlmap:
        print("The mapfile not found.")
        exit()
    #debug("urlmap", urlmap)
    while True:
        url = raw_input("\nPlease input url or Quit:\n")
        if url in opt:
            break
        if url in urlmap:
            filename = os.getcwd() + '/save/' + urlmap[url] + '.txt'
            with open(filename, 'r') as fd:
                for line in fd:
                    print line
        else:
            print("The url not found.")
        time.sleep(0.5)

if __name__ == '__main__':
    search()

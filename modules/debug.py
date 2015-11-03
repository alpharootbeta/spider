#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################


def debug(arg1, *args):
    """
    打印debug信息
    """
    list = []
    print '[debug>>>]',
    list.append(str(arg1))
    for arg in args:
        list.append(str(arg))
    getstr = ' : '.join(list)
    print getstr

if __name__ == '__main__':
    debug('debug log')
    debug('debug log', 22)
    debug('debug log', 22, debug)

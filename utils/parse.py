#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################

import pprint

def parse(line):
    """
    """
    ret = []
    index, start, end = 0, 0, 0
    length = len(line)
    while True:
        if line[index] == '"':
            index = index + 1
            end = index + line[index:].find('"')
            ret.append(line[index:end])
            index = end + 1
            start = end + 2
        elif line[index] == ' ':
            ret.append(line[start:index])
            start = index + 1
        index = index + 1
        if index >= length:
            break
    return ret


def test():
    s = '''2.051 NONE - 1.1.1.1 "-" www.example.com /data/small.jpg GET "Tengine<||>-" 404 "-" "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0" "zh-CN,zh;q=0.5<||>-" "sid18915=96ab1ba4; visit18915=35; last18915=1430279909;" "-"'''
    ret = parse(s)
    pprint.pprint(ret)

if __name__ == '__main__':
    test()

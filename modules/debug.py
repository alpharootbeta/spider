# coding: utf-8

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

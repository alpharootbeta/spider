#!/usr/bin/env python
# coding: utf-8

import os
import gzip
import cPickle

from debug import debug

class SerializeError(Exception):

    """
    docstring for SerializeError
    """
    pass


def serialize_object(filename, *obj):
    """
    序列化
    """
    if os.path.exists(filename):
        os.remove(filename)
    try:
        # 利用gzip节省存储空间
        fd = gzip.open(filename, "wb")
        for x in obj:
            cPickle.dump(x, fd)
        fd.close()
    except IOError:
        raise SerializeError


def unserialize_object(filename):
    """
    反序列
    """
    obj = {}
    if os.path.exists(filename):
        try:
            fd = gzip.open(filename, "rb")
            while True:
                try:
                    obj = cPickle.load(fd)
                except EOFError:
                    break
            fd.close()
        except IOError:
            raise SerializeError
    return obj


def test():
    d = {"1": "z", "2": "w", "3": "y"}
    serialize_object("./save/seri.pickle", d)
    s = unserialize_object("./save/seri.pickle")
    debug(s)

if __name__ == '__main__':
    test()

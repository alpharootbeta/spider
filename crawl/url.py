#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
##         Author: wenyu1001@126.com              ##
####################################################

import re
import urllib

from modules.debug import debug


def get_urls(page):
    """
    匹配url
    """
    urls, tmp = [], []
    #patt = "<a.*?href=.*?<\/a>"
    patt = '"((http|ftp|file)s?://.*?)"'
    if not page:
        return urls
    else:
        page_tmp = page.replace(" ", "")
        re_cpl = re.compile(patt, re.I)
        tmp = re_cpl.findall(page_tmp)
        for x in tmp:
            urls.append(x[0])
        return urls


def test(url):
    l = []
    fu = urllib.urlopen(url)
    s = fu.read()
    l = get_urls(s)
    debug(l)

if __name__ == '__main__':
    url = "http://www.jxnu.edu.cn"
    test(url)

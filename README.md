# spider v1.0.0

编写一个页面抓取程序，抓取给定网站的页面。保存网站的 url 列表，并将抓到的每个页面单独存成文件。

#### Detail

#### Design

* 采用多线程方式抓取页面

* 页面抓取采用广度遍历算法

* 采用命令行设定程序必要的参数

* 程序实时记录日志信息

* 抓取的页面实时保存

* url 序列化存储

* url 反序列化加载

* debug 调试选项

#### Usage

```
# normal mode
python spider.py -u http://www.sina.com.cn -d 3 -p 1000

# debug mode
python spider.py -u http://www.sina.com.cn --debug

# locate
python search.py
```

#### TODO

* gevent 替换 multithreading

* argparse 替换 optparse

* dupefilter 去重

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 03 17:10:50 2017

@author: dou
"""
import urllib2
import time


def down_png():
    url = "https://www.cqccms.com.cn/workspace/Captcha.jpg"
    for j in range(1000):
        open("" + str(j) + '.jpg', 'wb').write(urllib2.urlopen(url).read())
        time.sleep(0.02)
if __name__ == '__main__':
    down_png()


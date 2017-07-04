# -*- coding: utf-8 -*-
"""
Created on Tue Jul 03 20:10:50 2017

@author: dou
"""
from PIL import Image
import os


def binary(pic_f, saved_f):
    for pic in os.listdir(pic_f):
        img0 = Image.open(pic_f+pic)
        img = img0.convert("RGBA")
        pixdata = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if 0 < pixdata[x, y][0] < 30 and 0 < pixdata[x, y][1] < 30 and 0 < pixdata[x, y][2] < 30:
                    pixdata[x, y] = (255, 255, 255, 255)
                elif 210 < pixdata[x, y][0] and 210 < pixdata[x, y][1] and 210 < pixdata[x, y][2]:
                    pixdata[x, y] = (255, 255, 255, 255)
                elif 15 < pixdata[x, y][0] < 40 and 120 < pixdata[x, y][1] < 160 and 70 < pixdata[x, y][2] <100:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(saved_f+pic)


def set_table(a):
    table = []
    for i in range(256):
        if i < a:
            table.append(0)
        else:
            table.append(1)
    return table


def gray(pic_f, saved_f):
    for pic in os.listdir(pic_f):
        img0 = Image.open(pic_f+pic)
        img1 = img0.convert('L')
        img2 = img1.point(set_table(180), '1')
        img2.save(saved_f+pic)


def separate(pic_f, saved_f):
    box1 = (23, 0, 46, 118)
    box2 = (47, 0, 70, 118)
    box3 = (71, 0, 94, 118)
    box4 = (95, 0, 118, 118)
    for pic in os.listdir(pic_f):
        img0 = Image.open(pic_f+pic)
        roi_1 = img0.crop(box1)
        roi_2 = img0.crop(box2)
        roi_3 = img0.crop(box3)
        roi_4 = img0.crop(box4)
        roi_1.save(saved_f+'1_'+pic)
        roi_2.save(saved_f + '2_' + pic)
        roi_3.save(saved_f + '3_' + pic)
        roi_4.save(saved_f + '4_' + pic)

if __name__ == '__main__':
    binary('pic_4/', 'pic_4_binary/')
    gray('pic_4_binary/', 'pic_gray/')
    separate('pic_gray/', 'pic_sep/')

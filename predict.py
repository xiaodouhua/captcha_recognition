from PIL import Image
from sklearn.externals import joblib
import numpy as np
from pylab import array


def binary(pic_f):

    img0 = Image.open(pic_f)
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
    #img.show()
    return img


def set_table(a):
    table = []
    for i in range(256):
        if i < a:
            table.append(0)
        else:
            table.append(1)
    return table


def gray(pic_f):

    img0 = pic_f
    img1 = img0.convert('L')
    img2 = img1.point(set_table(180), '1')
    img2.save('tmp.jpg')
    return img2


def separate(pic_f):
    box1 = (23, 0, 46, 118)
    box2 = (47, 0, 70, 118)
    box3 = (71, 0, 94, 118)
    box4 = (95, 0, 118, 118)
    img0 = Image.open('tmp.jpg')
    roi_1 = img0.crop(box1)
    roi_2 = img0.crop(box2)
    roi_3 = img0.crop(box3)
    roi_4 = img0.crop(box4)
    roi_1.show()
    roi_2.show()
    roi_3.show()
    roi_4.show()
    return roi_1, roi_2, roi_3, roi_4

if __name__ == '__main__':
    img = binary('7.jpg')
    img2 = gray(img)
    data0, data1, data2, data3 = separate(img2)
    pca = joblib.load("pca.model")
    clf = joblib.load("clf.model")
    #print(data0)
    #print(array(data0))
    #print(np.array(array(data0)))
    data00 = np.array(array(data0)).reshape((1, -1))
    data10 = np.array(array(data1)).reshape((1, -1))
    data20 = np.array(array(data2)).reshape((1, -1))
    data30 = np.array(array(data3)).reshape((1, -1))

    data000 = pca.transform(data00)
    data100 = pca.transform(data10)
    data200 = pca.transform(data20)
    data300 = pca.transform(data30)

    a = clf.predict(data000)
    b = clf.predict(data100)
    c = clf.predict(data200)
    d = clf.predict(data300)
    print (a[0]+b[0]+c[0]+d[0])

# -*- coding: utf-8 -*-
 
from scipy import linalg, dot
from PIL import Image
 
def main(num=5):
    im = Image.open('me.png')
    pix = im.load()
    ma = [[], [], []]
    for x in xrange(im.size[0]):
        for i in xrange(3):
            ma[i].append([])
        for y in xrange(im.size[1]):
            for i in xrange(3):
                ma[i][-1].append(pix[x, y][i])
    for i in xrange(3):
        u, s, v = linalg.svd(ma[i])
        u = u[:, :num]
        v = v[:num, :]
        s = s[:num]
        ma[i] = dot(dot(u, linalg.diagsvd(s, num, num)), v)
    for x in xrange(im.size[0]):
        for y in xrange(im.size[1]):
            ret = []
            for i in xrange(3):
                tmp = int(ma[i][x][y])
                if tmp < 0:
                    tmp = 0
                if tmp > 255:
                    tmp = 255
                ret.append(tmp)
            pix[x, y] = tuple(ret)
    #im.show()
    im.save('me_%d.jpg' % num)
 
if __name__ == '__main__':
    for i in range(50):
        main(9 + i)
    


#-*- coding: utf-8 -*-

from PIL import Image
import random
import math

def flip_angle(im):
    w = im.size[0]
    h = im.size[1]
    box_left_top = (0, 0, w/2-1, h/2-1)
    box_right_bottom = (w/2, h/2, w-1, h-1)
    im_res = im.copy()
    im_res.paste(im.crop(box_left_top), box_right_bottom)
    im_res.paste(im.crop(box_right_bottom), box_left_top)
    return im_res

def remove_red(im):
    r, g, b, a = im.split()
    r = r.point(lambda v: 0)
    return Image.merge('RGBA', (r, g, b, a))

def darker(im):
    return Image.eval(im, lambda v: v * 0.5)

def make_alpha(im):
    r, g, b, a = im.split()
    a = a.point(lambda v: 155)
    return Image.merge('RGBA', (r, g, b, a))

def rand_img():
    im = Image.new('RGB', (64,128), 'white')
    pixel = im.load()
    rand = lambda : random.randint(0, 255)
    for c in range(im.size[0]):
        for r in range(im.size[1]):
            if r < im.size[1] / 2:
                pixel[c, r] = (rand(), rand(), rand())
            else:
                pixel[c, r] = (r, c, 0)
    return im

def fn_img(fn):
    row = 512
    col = 1024
    im = Image.new('RGB', (col, row), 'white')
    pixel = im.load()
    rand = lambda : random.randint(0, 255)
    for c in range(col):
        for r in range(row):
            pixel[c,r] = (0,0,0)
    for x in range(col):
        y = row - int(fn(x))
        for offset in range(-2, 2):
            yt = max(min(y + offset, row - 1), 0)
            pixel[x, yt] = (255,255,255)
    return im

def make_white_part_alpha(im, grey_scale_as_white = 200):
    pixel = im.load()
    rand = lambda : random.randint(0, 255)
    for c in range(im.size[0]):
        for r in range(im.size[1]):
            p = pixel[c,r]
            if (p[0] + p[1] + p[2]) / 3 > grey_scale_as_white:
                pixel[c,r] = (0,0,0,0) #(p[0], p[1], p[2], 0)
            else:
                pixel[c,r] = (p[0],p[1],p[2],p[3])
    return im

def rand_alpha(im):
    def gs(v):
        rv = random.random()
        if rv < 0.3:
            return random.randint(0, 100)
        return v
    source = im.split()
    a = source[-1].point(gs)
    source[-1].paste(a)
    return Image.merge('RGBA', source)

im = Image.open('avatar.png')
if im.mode != 'RGBA':
    im = im.convert('RGBA')

fn_img(lambda x: math.sin(x * 0.02) * 155 + 255).save('a.png')







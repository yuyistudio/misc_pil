#-*- coding: utf-8 -*-

import PIL
from PIL import Image, ImageFilter
class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"
    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds
    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

def GenerateHDRImage(input_filename, output_filename):
    image = Image.open(input_filename)
    size = image.size
    blur_pixels = int(size[0] * 0.5)
    new_size = (blur_pixels * 4 + size[0], blur_pixels * 4 + size[1])
    image_blur = Image.new('RGBA', new_size)
    image_blur.paste(image, (blur_pixels * 2, 2 * blur_pixels), image)
    result_image = image_blur.copy()
    bounding = (0, 0, new_size[0], new_size[1])

    image_blur_little = image_blur.copy().filter(MyGaussianBlur(radius=5, bounds=bounding))
    image_blur_big = image_blur.copy().filter(MyGaussianBlur(radius=int(blur_pixels), bounds=bounding))


    import math
    def merge_blur(*imgs):
        factors_common = [2, 2.5, 2.5]
        factors_diff = [0, 15, 15]
        size = len(imgs)
        pixels = [img.load() for img in imgs]
        def trans(c):
            # clamp
            c = [max(0,min(255,v)) for v in c]
            # get factor
            f = sum(c) / 3
            f = (math.cos(f / 255 * 2 * math.pi) + 1)
            f *= f
            f *= 0.25
            # return
            res = [c[0]*f, c[1]*f, c[2]*f, c[3]]
            return [int(v) for v in res]
        for x in range(imgs[0].size[0]):
            for y in range(imgs[0].size[1]):
                colors = [pixel[x, y] for pixel in pixels]
                c = []
                alpha_origin = colors[0][3]
                if alpha_origin > 100:# 重叠部分
                    factors = factors_common
                else:# 辉光部分
                    factors = factors_diff
                for i in range(3):
                    v = 0
                    for k in range(len(factors)):
                        v += colors[k][i] * factors[k]
                    c.append(int(v * 0.33))
                if alpha_origin > 100:
                    alpha = alpha_origin
                else:
                    alpha = sum(c) / 3 * 1.5

                #alpha = 255

                c.append(int(alpha))
                pixels[0][x, y] = tuple(trans(c))

    merge_blur(result_image, image_blur_big, image_blur_little)
    result_image.save(output_filename)

GenerateHDRImage('input.png', 'output.png')
#!/usr/bin/python
# written by s3rb31@mail.ru

import sys
from PIL import Image
from PIL import ImageEnhance

def image_identify_num(img):
    hi_num = -1
    hi_count = 0

    for i in xrange(1, 10):			
        count = image_pixel_equality(img, Image.open("tmpl/" + str(i) + "_b.png").convert("RGB"))
        if count > hi_count:
            hi_num = i
            hi_count = count

    return hi_num

def image_get_next_whitespace(start, img):
    white_xpos = -1
    white_count = 1
    
    pixdata = img.load()
    
    for x in xrange(start, img.size[0]):
        for y in xrange(img.size[1]):
            if pixdata[x,y] == (255, 255, 255):
                white_count += 1
            else:
                white_count = 0
        if white_count > (img.size[1] * 2):
            white_xpos = x
            break
            
    return white_xpos

def image_get_char(img):
    loX = -1; hiX = -1
    loY = -1; hiY = -1
    pixdata = img.load()
    
    for x in xrange(img.size[0]):
	#print pixel[x][0]
        for y in xrange(img.size[1]):
            if (pixdata[x, y] == (0, 0, 0)):
                if loX == -1 or loX > x: loX = x
                if hiX == -1 or hiX < x: hiX = x
                if loY == -1 or loY > y: loY = y
                if hiY == -1 or hiY < y: hiY = y
		
    return img.crop((loX, loY, hiX, hiY))


def image_pixel_equality(src_img, tpl_img):
    equality_count = 0

    w = src_img.size[0] if (src_img.size[0] <= tpl_img.size[0]) else tpl_img.size[0]
    h = src_img.size[1] if (src_img.size[1] <= tpl_img.size[1]) else tpl_img.size[1]

    tpl_img = tpl_img.crop((0, 0, w, h)).convert("RGB")
    
    pixdata_s = src_img.load();
    pixdata_c = tpl_img.load()
    
    for x in xrange(w):
        for y in xrange(h):
            if pixdata_s[x, y] == pixdata_c[x, y]:                
                equality_count += 1;
            if pixdata_s[x, y] != pixdata_c[x, y]:
                equality_count -= 1;
            
    return equality_count

def solve_captcha(img):
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.7)

    pixdata = img.load()

    for x in xrange(img.size[0]):
        for y in xrange(img.size[1]):
            if (    (pixdata[x,y][0] < 60 or pixdata[x,y][0] > 65)
                and (pixdata[x,y][1] < 60 or pixdata[x,y][0] > 65)
                and (pixdata[x,y][2] < 60 or pixdata[x,y][0] > 65)):
                    pixdata[x,y] = (255, 255, 255)
            else:
                pixdata[x,y] = (0, 0, 0)

    img = img.resize((600, 200), Image.NEAREST)

    pixdata = img.load()
	  
    for x in xrange(1, img.size[0] - 1):    
        for y in xrange(1, img.size[1] - 1):
            if pixdata[x,y] != (0, 0, 0):
                if (    (pixdata[x+1,y] == (0, 0, 0) and pixdata[x-1,y] == (0, 0, 0))
                    and (pixdata[x,y+1] == (0, 0, 0) or  pixdata[x,y-1] == (0, 0, 0))):
                    pixdata[x,y] = (0, 0, 0)
                if (    (pixdata[x,y+1] == (0, 0, 0) and pixdata[x,y-1] == (0, 0, 0))
                    and (pixdata[x+1,y] == (0, 0, 0) or  pixdata[x-1,y] == (0, 0, 0))):
                    pixdata[x,y] = (0, 0, 0)    
    
    exit_loop = 0
    img_count = 0
    captcha_val = ""
    
    for x in xrange(img.size[0]):
        if exit_loop == 1: break
        for y in xrange(img.size[1]):
            if exit_loop == 1: break            
            if pixdata[x, y] == (0, 0, 0):
                white_xpos = image_get_next_whitespace(x, img)                
                if white_xpos == -1:
                    exit_loop = 1
                    captcha_val = "error"
                else:
                    img_count += 1
                    
                    if x > 15: x -= 15
                    if img.size[1] - white_xpos >= 10: white_xpos += 10

                    captcha_val += str(image_identify_num(image_get_char(img.crop((x, 0, white_xpos, img.size[1])))))

                    if img_count == 5:                      
                        exit_loop = 1
                    else:
                        img = img.crop((white_xpos, 0, img.size[0], img.size[1]))
                        pixdata = img.load()
                        x = 0; y = 0

    return captcha_val

if __name__ == "__main__":
    img = Image.open("test.png")
    print solve_captcha(img)    

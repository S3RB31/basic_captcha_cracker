#!/usr/bin/python
# written by s3rb31@mail.ru

from PIL import Image
from solve_captcha import *

import re
import sys
import urllib
import urllib2
import cookielib
import StringIO

host = "https://www.paysafecard.com"
cookies = cookielib.CookieJar()

opener = urllib2.build_opener(
    urllib2.HTTPRedirectHandler(),
    urllib2.HTTPHandler(debuglevel=0),
    urllib2.HTTPSHandler(debuglevel=0),
    urllib2.HTTPCookieProcessor(cookies))

opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WinS3; x64) AppleWebKit/013.37 (KHTML, like Gecko) Chrome/45.0.2451.0 Safari/537.36')]

def get_captcha(file):
    url = host + "/fileadmin/source/widgets/balancecheck/lib/captcha/" + file    
    captcha_response = opener.open(url)

    buff = StringIO.StringIO()
    buff.write(captcha_response.read())
    buff.seek(0)

    img = Image.open(buff)
    img.save("captcha.png", "png")

    return img

def check_psc():
    url = host + "/fileadmin/source/widgets/balancecheck/index.php"
    response = opener.open(url)

    try:
        sid = re.search("securimage_show\.php\?sid=[0-9a-f]{40}", response.read()).group(0)
    except (AttributeError, IndexError):
        print "Could not find captcha SID! Mail to s3rb31@mail.ru ..."
        sys.exit()

    captcha_answer = solve_captcha(get_captcha(sid))

    print "Calculated captcha response:",captcha_answer
    
    values = {'cardnumber0' : '0918', 
              'cardnumber1' : '3234',
              'cardnumber2' : '4895',
              'cardnumber3' : '4136',
              'captcha' : captcha_answer,
              'action'	: '2',
              'lc'	: 'en-us'}

    response = opener.open(url, urllib.urlencode(values))

    try:
        value = re.search("Your paysafecard credit: (.*)<", response.read()).group(0)
    except (AttributeError, IndexError):
        print "Could not find PaySafeCard value! Retry ..."
        return check_psc()

    return value[:-1]

if __name__ == "__main__":
    print check_psc()

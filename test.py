#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

files = {
    'file': open('face/yammember2014.jpg', 'rb'),
    'face': '0'  # 0 for False, 1 for True
}

r = requests.post('http://0.0.0.0:8080/detect', files=files)

print r.text

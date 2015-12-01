#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import cv2 as cv
import requests
from StringIO import StringIO
from skimage import io

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    img = cv.resize(frame,
                    (frame.shape[1] / 2, frame.shape[0] / 2))
    # frame = frame[:, :, ::-1]

    s = StringIO()
    io.imsave(s, img, plugin='pil')
    s.seek(0)

    files = {
        'file': s,
        'face': '0'  # 0 for False, 1 for True
    }

    r = requests.post('http://10.8.0.112:8080/detect', files=files)
    results = json.loads(r.text)

    for ret in results:
        cls = ret['label']
        x1, y1, x2, y2 = ret['bbox']
        # draw label
        t_size, b = cv.getTextSize(cls, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2,
                     cv.CV_AA)
        cv.rectangle(img, (x1, y2 - t_size[1] - b),
                     (x1 + t_size[0], y2), (255, 0, 0), -1, cv.CV_AA)
        cv.putText(img, cls, (x1, y2 - b / 2), cv.FONT_HERSHEY_SIMPLEX,
                   1.0, (255, 255, 255), 1, cv.CV_AA)

    cv.imshow('frame', img)

    key = cv.waitKey(1)
    if key == 27:
        break

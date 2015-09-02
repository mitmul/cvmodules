#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 as cv


class FaceDetector(object):

    def __init__(self):
        cascade_fn = 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv.CascadeClassifier(cascade_fn)

    def detect_face(self, img):
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

        return faces

    def draw_face_rects(self, img):
        faces = self.detect_face(img)
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return img

if __name__ == '__main__':
    img = cv.imread('yammember2014.jpg')

    fd = FaceDetector()
    img = fd.draw_face_rects(img)
    cv.imwrite('yammember2014_faces.jpg', img)

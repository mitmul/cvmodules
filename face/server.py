#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from skimage import io
from StringIO import StringIO
from bottle import route, run, request
from detect import FaceDetector
from age_gender import AgeGender

face_detector = FaceDetector()
age_gender = AgeGender()


@route('/face', method='POST')
def face():
    """
    Pass a person bouding box to this method
    """
    try:
        image = request.files.get('file')
        img = io.imread(StringIO(image.file.read()))

        results = []
        faces = face_detector.detect_face(img)
        for (x, y, w, h) in faces:
            face = img[y:y + h, x:x + w, :3]
            age, gender = age_gender.get_age_gender(face)
            results.append({
                "age": age,
                "gender": gender
            })

        return json.dumps(results)

    except Exception as e:
        print str(type(e)), e

run(host='0.0.0.0', port=8082, debug=True, reloader=True)

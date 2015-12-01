#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if 'linux' in sys.platform:
    import matplotlib
    matplotlib.use('Agg')
import json
import requests
from skimage import io
from StringIO import StringIO
from bottle import route, run, request
import matplotlib.pyplot as plt

OBJ_SERVER = '0.0.0.0:8081'
FACE_SERVER = '0.0.0.0:8082'


@route('/detect', method='POST')
def detect():
    try:
        image = request.files.get('file')
        recog_face = bool(int(request.files.get('face').file.read()))
        files = {'file': StringIO(image.file.read())}
        objs = requests.post('http://{}/object'.format(OBJ_SERVER),
                             files=files)
        objs = json.loads(objs.text)

        print recog_face
        if recog_face:
            img = None
            for bb in objs:
                if bb['label'] == 'person':
                    if img is None:
                        image.file.seek(0)
                        img = io.imread(StringIO(image.file.read()))
                    x1, y1, x2, y2 = bb['bbox']
                    person_img = img[y1:y2, x1:x2]

                    # detect face
                    s = StringIO()
                    plt.imsave(s, person_img)
                    s.seek(0)
                    faces = requests.post('http://{}/face'.format(FACE_SERVER),
                                          files={'file': s})
                    bb['face'] = json.loads(faces.text)

        return json.dumps(objs)

    except Exception as e:
        print str(type(e)), e

run(host='0.0.0.0', port=8080, debug=True, reloader=True)

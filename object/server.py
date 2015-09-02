#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from bottle import route, run, request
from detect import FastRCNNPrediction
from skimage import io

fast_rcnn = FastRCNNPrediction()


@route('/object', method='POST')
def object():
    try:
        image = request.files.get('file')
        img = io.imread(StringIO(image.file.read()))

        results = fast_rcnn.detect(img)

        return json.dumps(results)

    except Exception as e:
        print str(type(e)), e

run(host='0.0.0.0', port=8081, debug=True, reloader=True)

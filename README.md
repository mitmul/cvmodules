# cvmodules for PRINTEPS

## Build Docker Image

```
$ bash build.sh
```

## Run Object Detection Server

```
$ bash run.sh 0
```

- The last digit indicates GPU ID.
- A request should be sent to `http://[IP Address]:3800[GPU ID]/detect` by POST method.
- See the example of sending image and visualizing results in `cvmodules/test.py`

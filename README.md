pyOSCapi
========

Python API to interact with network devices using the [Open Spherical Camera API](https://developers.google.com/streetview/open-spherical-camera/).

Documentation
=============

### Connect
```python
>>> from pyOSCapi import OSCAPI as OSC
>>> cam = OSC(ip="192.168.0.100", port="80")
>>> cam.connect()
```
The settings to connect differ from manufacturer to manufacturer:

* [Bublcam](http://bublcam.com/) `cam = OSC(ip="192.168.0.100", port="80")`
* [RICO THETA](https://theta360.com)  `cam = OSC(ip="192.168.1.1", port="80")`

### Do Stuff
```python
>>> cam.info()
```
### Close Connection
```python
>>> cam.disconnect()
```

License
=======

Copyright 2015 Florian Lehner

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0

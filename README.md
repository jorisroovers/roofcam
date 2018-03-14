# roofcam
Detecting water on my roof using a hi3510/rtt-3300 camera.

For now this is just some random code, but over time it will hopefully become something coherent :)

The goal is to have a cronjob that periodically takes snapshots using the camera pointed at my flat roof.
Roofcam will then detect whether the latest snapshot contains any water and then serve that snapshot and its
classification (water/no water) in a simple html page that can be included in a
[homeassistant](http://homeassistant.io/) dashboard.

Might also build a simple web UI to easily classify snapshots manually. The result of that manual classification
can then be compared to roofcam's classifier as to get an idea of roofcam's classifier accuracy. This will help to
experiment with different classifiers and compare their accuracy.

## Getting started

Roofcam requires [Pillow](http://pillow.readthedocs.io/en/4.0.x/index.html). Since Pillow has binary dependencies, it's
easiest to install it as a system package:

```bash
# Build container image
docker build -t roofcam .

# Run container
docker run -v $(pwd):/roofcam -p 1234:1234 -it roofcam bash

# setup.py develop needed to use Flask debug mode:
python setup.py develop

# Classify a single snapshot
roofcam-ml classify --debug -p `ls samples/snapshot* | sort | tail -1`

# Classify a directory of snapshots
roofcam-ml classify --debug -p samples

# host a webserver with the latest snapshot
roofcam --debug --dir samples --port 1234 --host 0.0.0.0
```

### Convenience commands

```bash
# Remove docker image
docker rmi -f roofcam
```

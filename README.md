# roofcam
Detecting water on my roof using a hi3510/rtt-3300 camera.

For now this is just some random code, but over time it will hopefully become something coherent :)

The goal is to have this serve the latest snapshot from my roof, detect whether that image contains any water and then
serve the snapshot and its classification in a simple html page that can be included in a home-assistant dashboard.

Might also build a simple web UI to manually classify snapshots as to get an idea of the automated water classifier
accuracy.


## Getting started

Roofcam requires [Pillow](http://pillow.readthedocs.io/en/4.0.x/index.html). Since Pillow has binary dependencies, it's
easiest to install it as a system package:

On Ubuntu:
```
sudo apt-get install python-imaging
```

Then:
```
pip install -r requirements.txt

# Classify a single snapshot
python -m roofcam.cli --file samples/`ls *samples* | sort | tail -1`

# Classify a directory of snapshots
python -m roofcam.cli --dir samples

# host a webserver with the latest snapshot
python -m roofcam.cli --dir samples --web --port 1234 --host localhost
```

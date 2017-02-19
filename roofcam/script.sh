#!/bin/bash

cd /home/pi/roofcam
ping -c 5 192.168.1.136 && curl "http://192.168.1.136/web/cgi-bin/hi3510/snap.cgi?&-getstream&-s" > snapshot-$(date +%Y-%m-%d_%H-%M-%S).jpg



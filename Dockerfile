FROM ubuntu:17.10

RUN apt-get update
RUN apt-get install -y python-imaging python-pip curl

ADD . /roofcam
WORKDIR /roofcam

RUN pip install -r /roofcam/requirements.txt
RUN python setup.py develop

EXPOSE 1234
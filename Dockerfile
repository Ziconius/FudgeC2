FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive

ENV CUSTOM_APPS="python3-pip"



RUN apt-get update && apt-get install --reinstall -yqq --allow-unauthenticated \
      $CUSTOM_APPS \
    && apt-get -y clean \
    && apt-get -y autoremove
#RUN apt update -y
#RUN apt upgrade -y
#RUN apt install --fix-broken
#RUN apt-mark unhold *

COPY FudgeC2/ /opt/FudgeC2/
WORKDIR /opt/FudgeC2

#RUN apt install -y python3-pip
RUN pip3 install -r /opt/FudgeC2/requirements.txt

CMD ["python3", "Controller.py"]
#RUN touch /a.txt
#CMD ["tail","-F","/a.txt"]


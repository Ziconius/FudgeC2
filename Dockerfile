FROM kalilinux/kali-rolling
COPY FudgeC2 /opt/FudgeC2
WORKDIR /opt/FudgeC2
RUN apt update \&& \
 apt install python3 python3-pip -y && \
 pip3 install -r requirements.txt
CMD python3 Controller.py

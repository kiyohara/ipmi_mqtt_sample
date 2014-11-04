# FROM kiyohara/docker-python
FROM kiyohara/docker-python-sshd

MAINTAINER Tomokazu Kiyohara <tomokazu.kiyohara@gmail.com>

### supervisor
# RUN apt-get -y install supervisor
# RUN mkdir -p /var/log/supervisor
# ADD etc/supervisor/conf.d/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

### ipmi_mqtt_sample
RUN apt-get install -y freeipmi

RUN pip install paho-mqtt

ADD ipmi-poll.sh /usr/local/bin/ipmi-poll.sh
ADD mqtt-pub.py /usr/local/bin/mqtt-pub.py

RUN rm -rf /tmp/ipmi_mqtt_sample

ADD etc/supervisor/conf.d/ipmi-mqtt.conf /etc/supervisor/conf.d/ipmi-mqtt.conf

CMD [ "/usr/bin/supervisord" ]

FROM kiyohara/docker-python

MAINTAINER Tomokazu Kiyohara <tomokazu.kiyohara@gmail.com>

### supervisor
RUN apt-get -y install supervisor
RUN mkdir -p /var/log/supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

### ipmi_mqtt_sample
RUN apt-get install -y freeipmi

RUN pip install paho-mqtt

# RUN git clone https://github.com/kiyohara/ipmi_mqtt_sample.git /tmp/ipmi_mqtt_sample
#
# RUN cp /tmp/ipmi_mqtt_sample/shell/*.sh /usr/local/bin/
# RUN cp /tmp/ipmi_mqtt_sample/shell/*.py /usr/local/bin/
ADD ipmi-poll.sh /usr/local/bin/ipmi-poll.sh
ADD mqtt-pub.py /usr/local/bin/mqtt-pub.py

RUN rm -rf /tmp/ipmi_mqtt_sample

CMD [ "/usr/bin/supervisord" ]

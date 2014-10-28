FROM kiyohara/docker-ruby

MAINTAINER Tomokazu Kiyohara <tomokazu.kiyohara@gmail.com>

RUN apt-get install -y ipmitool

RUN gem install --no-ri --no-rdoc rubyipmi
RUN gem install --no-ri --no-rdoc mqtt

RUN git clone https://github.com/kiyohara/ipmi_mqtt_sample.git /tmp/ipmi_mqtt_sample
RUN cd /tmp/ipmi_mqtt_sample/ruby; rake build
RUN gem install --no-ri --no-rdoc /tmp/ipmi_mqtt_sample/ruby/pkg/ipmi_mqtt_sample-*.gem
RUN rm -rf /tmp/ipmi_mqtt_sample

CMD [ "/usr/local/bin/ipmi_mqtt_sample" ]

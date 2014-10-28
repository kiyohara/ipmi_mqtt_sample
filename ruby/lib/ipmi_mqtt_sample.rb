require "ipmi_mqtt_sample/version"

module IpmiMqttSample
  IPMI_PROVIDER = 'ipmitool'

  $LOAD_PATH << File.expand_path(File.join(File.dirname(__FILE__)))

  require 'rubyipmi'
  require 'mqtt'

  require 'ipmi_mqtt_sample/worker'
end

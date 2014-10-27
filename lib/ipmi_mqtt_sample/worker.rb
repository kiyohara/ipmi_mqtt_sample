module IpmiMqttSample
  class Worker
    def initialize
      @ipmi_target = ENV['IPMI_TARGET'] || 'localhost'
      @ipmi_user   = ENV['IPMI_USER']
      @ipmi_pass   = ENV['IPMI_PASS']
      @mqtt_broker = ENV['MQTT_BROKER'] || 'localhost'
      @mqtt_topic  = ENV['MQTT_TOPIC'] || '/ipmi-mqtt-sample'
    end

    def run
      puts '--- IPMI-MQTT sample running ---'
      puts "IPMI_TARGET : #{@ipmi_target}"
      puts "  IPMI_USER : #{@ipmi_user}" if @ipmi_user
      puts "  IPMI_PASS : #{@ipmi_pass}" if @ipmi_pass
      puts "MQTT_BROKER : #{@mqtt_broker}"
      puts "MQTT_TOPIC  : #{@mqtt_topic}"

      ipmi_conn = Rubyipmi.connect(
        @ipmi_user,
        @ipmi_pass,
        @ipmi_target,
        IPMI_PROVIDER,
        {
          timeout: 30,
        }
      )

      loop do
        start_time = Time.now

        ipmi_res = ipmi_conn.chassis.power.status
        raise 'No IPMI response' unless ipmi_res

        end_time = Time.now
        rtt = end_time - start_time

        message = "[#{start_time}] Target #{@ipmi_target} res \"#{ipmi_res}\" - RTT: #{rtt}"

        MQTT::Client.connect(@mqtt_broker) do |c|
          puts "MQTT pub : Topic #{@mqtt_topic} : message \"#{message}\""
          c.publish(@mqtt_topic, message)
        end

        sleep 1
      end
    end
  end
end

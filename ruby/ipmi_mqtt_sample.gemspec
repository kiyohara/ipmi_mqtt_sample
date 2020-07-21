# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'ipmi_mqtt_sample/version'

Gem::Specification.new do |spec|
  spec.name          = "ipmi_mqtt_sample"
  spec.version       = IpmiMqttSample::VERSION
  spec.authors       = ["Tomokazu Kiyohara"]
  spec.email         = ["tomokazu.kiyohara@gmail.com"]
  spec.summary       = %q{IMPI power status to MQTT broker sample}
  spec.description   = %q{IMPI power status to MQTT broker sample}
  spec.homepage      = ""
  spec.license       = "MIT"

  spec.files         = `git ls-files -z`.split("\x0")
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.test_files    = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths = ["lib"]

  spec.add_runtime_dependency 'rubyipmi'
  spec.add_runtime_dependency 'mqtt'

  spec.add_development_dependency "bundler"
  spec.add_development_dependency "rake"
end

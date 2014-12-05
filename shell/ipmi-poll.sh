#!/bin/sh

export OUTPUT_DIR=/tmp/ipmi-poll
export ERR_DIR=/tmp/ipmi-poll-err

[ -d $OUTPUT_DIR ] || mkdir -p $OUTPUT_DIR
[ -d $ERR_DIR ] || mkdir -p $ERR_DIR

while true; do
  ipmi-sensors.sh
  ipmi-chassis.sh

  sleep 1
done

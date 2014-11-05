#!/bin/sh

EXEC_CMD=ipmi-sensors
OUTPUT_DIR=/tmp

if ! `which $EXEC_CMD 2>&1 > /dev/null`; then
  echo ERROR: freeipmi required
  exit 1
fi

[ -z "$IPMI_TARGET" ] && IPMI_TARGET=localhost
EXEC_ARGS="-h $IPMI_TARGET"
[ -n "$IPMI_USER" ] && EXEC_ARGS="$EXEC_ARGS -u $IPMI_USER"
[ -n "$IPMI_PASS" ] && EXEC_ARGS="$EXEC_ARGS -p $IPMI_PASS"
[ -n "$IPMI_SENSOR_TYPES" ] && EXEC_ARGS="$EXEC_ARGS --sensor-types=$IPMI_SENSOR_TYPES"

# EXEC_ARGS="$EXEC_ARGS --no-header-output --comma-separated-output"
EXEC_ARGS="$EXEC_ARGS --comma-separated-output"

while true; do
  # FILE_POSTFIX=`date +%Y%m%d-%H%M%S-%N`
  UNIX_TIME=`date +%s.%N` # unixtime w/ nano
  FILE_POSTFIX=$UNIX_TIME
  OUTPUT_FILE=$OUTPUT_DIR/$EXEC_CMD-$FILE_POSTFIX
  TEMP_FILE=`mktemp`

  echo $UNIX_TIME > $TEMP_FILE
  echo $IPMI_TARGET >> $TEMP_FILE
  $EXEC_CMD $EXEC_ARGS >> $TEMP_FILE
  if $?; then
    mv $TEMP_FILE $OUTPUT_FILE
  else
    mv $TEMP_FILE _err_${OUTPUT_FILE}
  fi

  sleep 1
done

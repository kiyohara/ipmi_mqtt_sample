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

# EXEC_ARGS="$EXEC_ARGS --no-header-output --comma-separated-output"
EXEC_ARGS="$EXEC_ARGS --comma-separated-output"

while true; do
  # FILE_POSTFIX=`date +%Y%m%d-%H%M%S-%N`
  FILE_POSTFIX=`date +%s` # unixtime
  OUTPUT_FILE=$OUTPUT_DIR/$EXEC_CMD-$FILE_POSTFIX

  $EXEC_CMD $EXEC_ARGS > $OUTPUT_FILE

  sleep 1
done

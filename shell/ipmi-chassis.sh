#!/bin/sh

EXEC_CMD=ipmi-chassis

if ! `which $EXEC_CMD 2>&1 > /dev/null`; then
  echo ERROR: freeipmi required
  exit 1
fi

[ -z "$IPMI_TARGET" ] && IPMI_TARGET=localhost
EXEC_ARGS="-h $IPMI_TARGET"
[ -n "$IPMI_USER" ] && EXEC_ARGS="$EXEC_ARGS -u $IPMI_USER"
[ -n "$IPMI_PASS" ] && EXEC_ARGS="$EXEC_ARGS -p $IPMI_PASS"

if [ -n "$IPMI_CHASSIS_COMMAND" ]; then
  EXEC_ARGS="$EXEC_ARGS $IPMI_CHASSIS_COMMAND"
else
  EXEC_ARGS="$EXEC_ARGS --get-chassis-status"
fi

[ -z "$OUTPUT_DIR" ] && OUTPUT_DIR=/tmp
[ -z "$ERR_DIR" ] && ERR_DIR=/tmp

[ -d $OUTPUT_DIR ] || mkdir -p $OUTPUT_DIR
[ -d $ERR_DIR ] || mkdir -p $ERR_DIR

# FILE_POSTFIX=`date +%Y%m%d-%H%M%S-%N`
UNIX_TIME=`date +%s.%N` # unixtime w/ nano
FILE_POSTFIX=$UNIX_TIME
OUTPUT_FILE_NAME=$EXEC_CMD-$FILE_POSTFIX
OUTPUT_FILE_PATH=$OUTPUT_DIR/$OUTPUT_FILE_NAME
TEMP_FILE=`mktemp`

echo $UNIX_TIME > $TEMP_FILE
echo $IPMI_TARGET >> $TEMP_FILE
$EXEC_CMD $EXEC_ARGS >> $TEMP_FILE
if [ $? -eq 0 ]; then
  mv $TEMP_FILE $OUTPUT_FILE_PATH
else
  mv $TEMP_FILE ${ERR_DIR}/${OUTPUT_FILE_NAME}
fi

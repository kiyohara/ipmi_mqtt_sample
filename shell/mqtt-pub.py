# coding: UTF-8

import os
import sys
import glob
import datetime
import time
import re
import csv
import json

import paho.mqtt.client as paho


#####


def is_debug():
    return (int(os.environ.get('DEBUG') or "0") > 0)


def is_disable_pub():
    return (int(os.environ.get('DISABLE_PUB') or "0") > 0)


def is_disable_loop():
    return (int(os.environ.get('DISABLE_LOOP') or "0") > 0)


def msg_log(msg):
    out = sys.stdout
    out.write("Log: {0}\n".format(msg))
    out.flush()


def msg_err(msg):
    out = sys.stderr
    out.write("Error: {0}\n".format(msg))
    out.flush()


def msg_debug(msg):
    if is_debug():
        out = sys.stdout
        out.write("Debug: {0}\n".format(msg))
        out.flush()


#####


def on_connect(client, obj, rc):
    #
    # result code:
    # https://pypi.python.org/pypi/paho-mqtt#connect-reconnect-disconnect
    #
    # 0: Connection successful
    # 1: Connection refused - incorrect protocol version
    # 2: Connection refused - invalid client identifier
    # 3: Connection refused - server unavailable
    # 4: Connection refused - bad username or password
    # 5: Connection refused - not authorised
    # 6-255: Currently unused.
    msg_log("Connection result: {0}".format(str(rc)))


def on_disconnect(client, obj, rc):
    #
    # result code:
    # https://pypi.python.org/pypi/paho-mqtt#callbacks
    #
    # If MQTT_ERR_SUCCESS (0), the callback was called in response to a
    # disconnect() call. If any other value the disconnection was unexpected,
    # such as might be caused by a network error.
    #
    if rc == 0:  # 正常切断時は NOP
        return

    msg_err("Unexpected disconnect: {0}".format(str(rc)))


def on_message(client, obj, msg):
    msg_debug("msg: {0} {1} {2}".format(msg.topic,
                                        str(msg.qos),
                                        str(msg.payload)))


def on_publish(client, obj, mid):
    msg_debug("published mid: {0}".format(str(mid)))


def mqtt_pub(mqtt, topic, data):
    # publish_time = time.time()
    publish_time = int(time.time())  # 小数点以下切捨(暫定仕様)

    message = {}
    message['publish_time'] = publish_time
    message['publish_data'] = data

    msg_debug("publish topic: {0}".format(topic))
    msg_debug("publish msg: {0}".format(json.dumps(message)))

    #
    # result code:
    # https://pypi.python.org/pypi/paho-mqtt#publishing
    #
    # Returns a tuple (result, mid), where result is MQTT_ERR_SUCCESS to
    # indicate success or MQTT_ERR_NO_CONN if the client is not currently
    # connected. mid is the message ID for the publish request.
    #
    (res, mid) = mqtt.publish(topic, json.dumps(message), qos=0)
    if res == paho.MQTT_ERR_SUCCESS:
        return True
    else:
        msg_debug("Publish: error: code({0})".format(str(res)))

        return False


def mqtt_pub_all(mqtt, ipmi_entries):
    return mqtt_pub(mqtt, '/all', ipmi_entries)


def mqtt_pub_split(mqtt, ipmi_entries):
    func_res = True
    for entry in ipmi_entries:
        target_ipaddr = entry['target_ipaddr'].replace('.', '_')
        capture_time = entry['capture_time']

        for i in entry['ipmi_data']:
            str_name = i['Name'].replace(' ', '_')
            str_type = i['Type'].replace(' ', '_')

            topic = '/ipmi/' + target_ipaddr + '/' + str_type + '/' + str_name

            data = {}
            data['target_ipaddr'] = target_ipaddr
            data['capture_time'] = capture_time
            data['ipmi_data'] = i

            pub_res = mqtt_pub(mqtt, topic, data)

            func_res = func_res and pub_res

    return func_res


def filename_to_datetime(file_name):
    dtime = datetime.datetime.fromtimestamp(filename_to_unixtime(file_name))
    strtime = dtime.strftime('%Y-%m-%d %H:%M:%S')
    print(strtime)


def filename_to_unixtime(file_name):
    utime = re.search(r'/ipmi-sensors-(\d+)', file_name).group(1)
    return float(utime)


def ipmi_file_parser(ipmi_file):
    with open(ipmi_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        result_data = {}
        # result_data['capture_time'] = next(reader).pop()
        result_data['capture_time'] = int(
            float(next(reader).pop())
        )  # 小数点以下切捨(暫定仕様)
        result_data['target_ipaddr'] = next(reader).pop()

        header = next(reader)

        ipmi_entry = {}
        ipmi_entries = []
        for row in reader:
            i = 0
            for value in row:
                ipmi_entry[header[i]] = value
                i += 1
            ipmi_entries.append(ipmi_entry)
            ipmi_entry = {}

        result_data['ipmi_data'] = ipmi_entries

    return result_data


def ipmi_files_handler(mqtt):
    if os.path.exists('./tmp/'):
        ipmi_files = glob.glob('./tmp/ipmi-sensors-*')
    else:
        ipmi_files = glob.glob('/tmp/ipmi-sensors-*')

    ipmi_entries = []
    for ipmi_file in ipmi_files:
        ipmi_entries.append(ipmi_file_parser(ipmi_file))

        # pub_res = mqtt_pub_all(mqtt, ipmi_entries)
        pub_res = mqtt_pub_split(mqtt, ipmi_entries)

        if not pub_res:
            msg_err("Publish: error: file: {0}".format(ipmi_file))
            next
        else:
            if not is_debug():
                os.remove(ipmi_file)


def main():
    mqtt_server_addr = os.environ.get('MQTT_SERVER_ADDR') or "127.0.0.1"

    mqtt = paho.Client()
    mqtt.on_connect = on_connect
    mqtt.on_disconnect = on_disconnect
    mqtt.on_message = on_message
    mqtt.on_publish = on_publish

    try:
        if is_disable_pub():
            msg_log("Skip connecting to MQTT server")
        else:
            msg_log("Connecting to MQTT server({0})".format(mqtt_server_addr))
            mqtt.connect(mqtt_server_addr, 1883, 60)
    except:
        msg_err("MQTT server: connection refused")
        return 1

    while True:
        ipmi_files_handler(mqtt)

        if is_disable_loop():
            break

        time.sleep(1)

main()

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


def DEBUG():
    return (int(os.environ.get('DEBUG') or "0") > 0)


def on_connect(client, obj, rc):
    print("connection result: {0}".format(str(rc)))
    sys.stdout.flush()


def on_message(client, obj, mesg):
    if not DEBUG():
        print("mesg: {0} {1} {2}".format(mesg.topic,
                                         str(mesg.qos),
                                         str(mesg.payload)))
        sys.stdout.flush()


def on_publish(client, obj, mid):
    if not DEBUG():
        print("Published mid: {0}".format(str(mid)))
        sys.stdout.flush()


def mqtt_pub(mqtt, topic, data):
    # publish_time = time.time()
    publish_time = int(time.time())  # 小数点以下切捨(暫定仕様)

    message = {}
    message['publish_time'] = publish_time
    message['publish_data'] = data

    if DEBUG():
        message['topic'] = topic
        print(json.dumps(message))
    else:
        mqtt.publish(topic, json.dumps(message), qos=0)


def mqtt_pub_all(mqtt, ipmi_entries):
    mqtt_pub(mqtt, '/all', ipmi_entries)


def mqtt_pub_split(mqtt, ipmi_entries):
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

            mqtt_pub(mqtt, topic, data)


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
        result_data['capture_time'] = int(next(reader).pop())  # 小数点以下切捨(暫定仕様)
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


def ipmi_files_handler(mqtt, prev_index):
    last_index = prev_index

    if os.path.exists('./tmp/'):
        ipmi_files = glob.glob('./tmp/ipmi-sensors-*')
    else:
        ipmi_files = glob.glob('/tmp/ipmi-sensors-*')

    ipmi_entries = []
    for ipmi_file in ipmi_files:
        target_index = filename_to_unixtime(ipmi_file)
        if target_index > prev_index:
            ipmi_entries.append(ipmi_file_parser(ipmi_file))
            last_index = target_index

    # mqtt_pub_all(mqtt, ipmi_entries)
    mqtt_pub_split(mqtt, ipmi_entries)

    for ipmi_file in ipmi_files:
        if not DEBUG():
            os.remove(ipmi_file)

    return last_index


def main():
    mqtt_server_addr = os.environ.get('MQTT_SERVER_ADDR') or "127.0.0.1"
    disable_loop = DEBUG() or (int(os.environ.get('DISABLE_LOOP') or "0") > 0)

    mqtt = paho.Client()
    mqtt.on_message = on_message
    mqtt.on_connect = on_connect
    mqtt.on_publish = on_publish

    try:
        if DEBUG():
            sys.stderr.write("DEBUG MODE: skip connect MQTT\n")
            sys.stderr.flush()
        else:
            mqtt.connect(mqtt_server_addr, 1883, 60)
    except:
        sys.stderr.write("MQTT server: connection refused\n")
        sys.stderr.flush()
        return 1

    last_index = 0

    while True:
        last_index = ipmi_files_handler(mqtt, last_index)

        if disable_loop:
            break

        time.sleep(1)

main()

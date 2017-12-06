#!/usr/bin/python3
import etcd3
import base64
import json
import pprint
import logging
import time

# value = b'foo'
# value64 = base64.b64encode(value)
# print("encoded %s" %value64)
# value = base64.b64decode(value64)
# print("decoded %s" %value)

class etcdtool:
    def __init__(self):
        self.dummy = 10

class thing:
    def __init__(self):
        self.pre_put = 0
        self.post_put = 0
        self.update_time = 0


def watch_callback(thing):
    #print("event: %s" %event)
    #print ("time %s" %time.time())
    thing.update_time = time.time()

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    logger.info("test logger")

    t1 = thing()

    h2 = etcd3.client(host='10.0.0.2', port=2379)
    h3 = etcd3.client(host='10.0.0.3', port=2379)
    h2.put("/WM/TempSensor/cpu/quota/", "100")
    watch_id = h3.add_watch_callback("/WM/TempSensor/cpu/quota/", watch_callback(thing))

    thing.pre_put = time.time()
    h2.put("/WM/TempSensor/cpu/quota/", "2000")
    thing.post_put = time.time()

    h3.cancel_watch(watch_id)

    logger.info("pre put time: %s" %thing.pre_put)
    logger.info("post put time: %s" %thing.post_put)
    logger.info("update time: %s" %thing.update_time)
    # thing = etcdtool()
    # print (thing.dummy)
    # with open ('./app/WeatherMonitor_app.json') as f:
    #     appJSON = json.load(f)
    # pprint.pprint(appJSON)


if __name__ == '__main__':
    main()

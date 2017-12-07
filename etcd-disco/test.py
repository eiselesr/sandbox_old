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

class stopWatch:
    def __init__(self):
        self.pre_put = 0
        self.post_put = 0
        self.update_time = 0
        self.pre_watch = 0

class devLogger:
    def __init__(self, lvl):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(lvl)
        self.logger.addHandler(self.ch)

def timeTest():
    time_log = devLogger(logging.WARN)

    sw1 = stopWatch()

    h2 = etcd3.client(host='10.0.0.2', port=2379)
    h3 = etcd3.client(host='10.0.0.3', port=2379)

    h2.put("/WM/TempSensor/cpu/quota/", "0")
    time_log.logger.info("get h2 value: %s" %(h2.get('/WM/TempSensor/cpu/quota/'))[0])

    def watch_callback(event):
        sw1.update_time = time.time()

    sw1.pre_watch = time.time()
    watch_id = h3.add_watch_callback("/WM/TempSensor/cpu/quota/", watch_callback)
    sw1.pre_put = time.time()
    h2.put("/WM/TempSensor/cpu/quota/", "500")
    sw1.post_put = time.time()
    time_log.logger.info("get h2 value: %s" %(h2.get('/WM/TempSensor/cpu/quota/'))[0])

    #need to wait for update to occur. Otherwise script finishes before callback.
    while(sw1.update_time ==0):
        pass

    h3.cancel_watch(watch_id)
    time_log.logger.info("pre watch time: %s" %sw1.pre_watch)
    time_log.logger.info("pre put time: %s" %sw1.pre_put)
    time_log.logger.info("post put time: %s" %sw1.post_put)
    time_log.logger.info("update time: %s" %sw1.update_time)

    time_log.logger.info("post_put - pre_put = %s" %(sw1.post_put - sw1.pre_put))
    time_log.logger.info("update_time - pre_put = %s" %(sw1.update_time - sw1.pre_put))
    time_log.logger.info("update_time - post_put = %s" %(sw1.update_time - sw1.post_put))

def flatten_json(y, name=''):
    '''flattens a json config file to enter to etcd as keys'''
    # https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '/')
        elif type(x) is list:
            #REMOVE SQUARE BRACKETS
            #a=','.join(map(str, x))
            #flatten(a, name + '/')
            # TURN DIRECTLY TO STRING
            a = str(x)
            flatten(a, name + '/')
            # KEY LEAVES WITH NUMERICAL INDEX
            # i = 0
            # for a in x:
                # flatten(a, name + str(i) + '/')
                # i += 1
        else:
            out[name[:-1]] = x

    flatten(y, name)
    return out

def loadJSON(path):
    ''' Loads a json into etcd'''

    h2 = etcd3.client(host='10.0.0.2', port=2379)
    h3 = etcd3.client(host='10.0.0.3', port=2379)

    json_log = devLogger(logging.DEBUG)
    with open (path) as f:
        appJSON = json.load(f)
    flat = flatten_json(appJSON, '/WM/')
    for key in flat:
        json_log.logger.info("%s : %s" %(key, flat[key]))
        h2.put(key, str(flat[key]))


def main():
    #loadJSON('./app/WeatherMonitor_app.json')

    #timeTest()
    pass

if __name__ == '__main__':
    main()

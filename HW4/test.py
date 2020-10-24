#!/usr/bin/python

"""
Ghozali, Oct 2020
"""

"""
@Student <Name/Matricno>
Date :
"""

import httplib
import json
import time as t
class flowStat(object):
    def __init__(self, server):
        self.server = server

    def get(self, switch):
        ret = self.rest_call({}, 'GET', switch)
        return json.loads(ret[2])

    def rest_call(self, data, action, switch):
        path = '/wm/core/switch/'+switch+"/flow/json"
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        # print path
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

flowget = flowStat('127.0.0.1')


if __name__ == '__main__':
    
    switching = 0
    retData = flowget.get("00:00:00:00:00:00:00:03")
    while (True):
        time_prev = 0
        time_after = 0
        byteCount_prev = 0
        byteCount_after = 0

        retData = flowget.get("00:00:00:00:00:00:00:03")
        myFlows = retData['flows']
        for myFlow in myFlows:
            myMatch = myFlow['match']
            if 'ipv4_src' not in myMatch:
                continue
            if 'ipv4_dst' not in myMatch:
                continue
            ipSrc = myMatch['ipv4_src']
            ipDst = myMatch['ipv4_dst']
            if (ipSrc == "10.0.0.1") and (ipDst == "10.0.0.3"):
                time_prev = myFlow['durationSeconds']
                byteCount_prev = myFlow['byteCount']
        print('durationSeconds_prev: ', time_prev)
        print('byteCount_prev: ', byteCount_prev)
        print('byteCount_prev: ', int(byteCount_prev))
        t.sleep(1)

        retData = flowget.get("00:00:00:00:00:00:00:03")
        myFlow = retData['flows']
        for myFlow in myFlows:
            myMatch = myFlow['match']
            if 'ipv4_src' not in myMatch:
                continue
            if 'ipv4_dst' not in myMatch:
                continue
            ipSrc = myMatch['ipv4_src']
            ipDst = myMatch['ipv4_dst']
            if (ipSrc == "10.0.0.1") and (ipDst == "10.0.0.3"):
                time_after = myFlow['durationSeconds']
                byteCount_after = myFlow['byteCount']

        if (time_prev == 0 or time_after == 0 or byteCount_prev == 0 or byteCount_after == 0):
            print("error!!")

        time = int(time_after) - int(time_prev)
        byteCount = int(byteCount_after) - int(byteCount_prev)

        if (time == 0):
            continue
        tp = byteCount * 8.0 / 1000000 / time
        print(t.time(), " throughput: ", tp, "Mbps")

    # print(retData)
    pass
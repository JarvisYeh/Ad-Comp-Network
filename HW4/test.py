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


def getStatics(switch_id):
    time = 0
    byteCount = 0

    retData = flowget.get(switch_id)
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
            time = int(myFlow['durationSeconds'])
            byteCount = int(myFlow['byteCount'])
    return time, byteCount
        


if __name__ == '__main__':

    while True:
        time_prev = 0
        time_after = 0
        byteCount_prev = 0
        byteCount_after = 0

        time_prev, byteCount_prev = getStatics("00:00:00:00:00:00:00:03")
        t.sleep(0.5)
        time_after, byteCount_after = getStatics("00:00:00:00:00:00:00:03")

        time = time_after - time_prev
        byteCount = byteCount_after - byteCount_prev

        if (time == 0):
            print("error!")
            break

        tp = byteCount * 8.0 / 1000000 / time
        print("duration: ", time,", "  " throughput: ", tp, "Mbps")

    # print(retData)
    pass
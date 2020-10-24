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
    retData = flowget.get("00:00:00:00:00:00:00:01")
    print(retData)
    pass
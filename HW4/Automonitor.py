
"""
@Student <Name/YE JIAWEI>
Date : Oct 24th
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

def getStatics(switch_id, src_ip, dest_ip):
    time = 0
    byteCount = 0
    packetCount = 0

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
        if (ipSrc == src_ip) and (ipDst == dest_ip):
            time = int(myFlow['durationSeconds'])
            byteCount = int(myFlow['byteCount'])
            packetCount = int(myFlow['packetCount'])

    return time, byteCount, packetCount

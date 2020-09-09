#!/usr/bin/python

"""
@Author <YE JIAWEI/A0212246R>
Date : 08/09/2020
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


class StaticFlowPusher(object):
    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        # print ret
        conn.close()
        return ret


pusher = StaticFlowPusher('127.0.0.1')
flowget = flowStat('127.0.0.1')


# To insert the policies for the traffic applicable to path between S1 and S2
def S1toS2():
    # h1->h2 has the rate limit of 1Mbps
    # need to set_queue to Queue 1
    # for both policy, add set_queue=2 to action key
    # set default maximum priority = 32767
    S1Limitflow = {
        'switch': "00:00:00:00:00:00:00:01",
        "name": "S1Limith1toh2",
        "cookie": "0",
        "priority": "32767",
        "in_port": "1",
        "eth_type": "0x800",
        "ipv4_src": "10.0.0.1",
        "ipv4_dst": "10.0.0.2",
        "active": "true",
        "actions": "set_queue=1,output=2"
    }

    S2Limitflow = {
        'switch': "00:00:00:00:00:00:00:02", 
        "name": "S2Limith1toh2", 
        "cookie": "0",
        "priority": "32767", 
        "in_port": "2", 
        "eth_type": "0x800", 
        "ipv4_src": "10.0.0.1",
        "ipv4_dst": "10.0.0.2", 
        "active": "true", 
        "actions": "set_queue=1,output=1"      
    }

    pusher.set(S1Limitflow)
    pusher.set(S2Limitflow)


# To insert the policies for the traffic applicable to path between S2 and S3
def S2toS3():
    # block all UDP port from 1000 - 1100
    # use udp_dst has the prerequisite ip_proto=0x11
    # set priority to default maximum=32767

    # policy for S3 from h3 to h2
    for port in range(1000, 1101) :
        name = "S3Blockh3toh2" + str(port)
        pusher.set({
            'switch': "00:00:00:00:00:00:00:03",
            "name": name,
            "cookie": "0",
            "priority": "32767",
            "in_port": "1",
            "eth_type": "0x800",
            "ipv4_src": "10.0.0.3",
            "ipv4_dst": "10.0.0.2",
            "ip_proto": "0x11",
            "udp_dst": str(port),
            "active": "true",
            "actions": ""
        })

    # policy for S3 from h2 to h3
    for port in range(1000, 1101) :
        name = "S3Blockh2toh3" + str(port)
        pusher.set({
            'switch': "00:00:00:00:00:00:00:03",
            "name": name,
            "cookie": "0",
            "priority": "32767",
            "in_port": "3",
            "eth_type": "0x800",
            "ipv4_src": "10.0.0.2",
            "ipv4_dst": "10.0.0.3",
            "ip_proto": "0x11",
            "udp_dst": str(port),
            "active": "true",
            "actions": ""
        })

    # policy for S2 from h3 to h2
    for port in range(1000, 1101) :
        name = "S2Blockh3toh2" + str(port)
        pusher.set({
            'switch': "00:00:00:00:00:00:00:02",
            "name": name,
            "cookie": "0",
            "priority": "32767",
            "in_port": "3",
            "eth_type": "0x800",
            "ipv4_src": "10.0.0.3",
            "ipv4_dst": "10.0.0.2",
            "ip_proto": "0x11",
            "udp_dst": str(port),
            "active": "true",
            "actions": ""
        })

    # policy for S2 from h2 to h3
    for port in range(1000, 1101) :
        name = "S2Blockh2toh3" + str(port)
        pusher.set({
            'switch': "00:00:00:00:00:00:00:02",
            "name": name,
            "cookie": "0",
            "priority": "32767",
            "in_port": "1",
            "eth_type": "0x800",
            "ipv4_src": "10.0.0.2",
            "ipv4_dst": "10.0.0.3",
            "ip_proto": "0x11",
            "udp_dst": str(port),
            "active": "true",
            "actions": ""
        })


# To insert the policies for the traffic applicable to path between S1 and S3
def S1toS3():
    # initialize the total_bit to 0
    total_bit = 0

    # priority of three different stages increases
    # total < 20Mb, policy priority = 32765
    # 20Mb <= total <= 30Mb, policy priority = 32766
    # 30Mb < total, total priority = 32767
    while total_bit <= 30 * 1024 * 1024:
        print str(total_bit/1024/1024) + "Mb transfered"
        # obtain response from swtich through rest api
        response = flowget.get("00:00:00:00:00:00:00:01")
        flows = response["flows"]

        # sum up target flows size
        for i in range(len(response["flows"])):
            print flows[i]["match"]
            print "eth_type" in flows[i]["match"]
            print "eth_type" in flows[i]["match"] and flows[i]["match"]["eth_type"] == "0x0x800"
            if checkMatch(flows[i]["match"]):
                print total_bit + str(total_byte)
                total_bit += int(flows[i]["byteCount"]) * 8
        
        if total_bit < 20 * 1024 * 1024:
            # for http request (tcp destination port 8080)
            # use tcp_dst has the prerequisite ip_proto=0x06

            # policy for S1 from h1 to h3
            # 1Mbps
            print "1Mbps"
            pusher.set({
                'switch': "00:00:00:00:00:00:00:01",
                "name": "S1Limit1Mh1toh3",
                "cookie": "0",
                "priority": "32765",
                "in_port": "1",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": "set_queue=1,output=3"
            })

            # policy for S3 from h1 to h3
            # 1Mbps
            pusher.set({
                'switch': "00:00:00:00:00:00:00:03",
                "name": "S3Limit1Mh1toh3",
                "cookie": "0",
                "priority": "32766",
                "in_port": "2",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": "set_queue=1,output=1"
            }) 
        elif total_bit >= 20 * 1024 * 1024 and total_bit <= 30 * 1024 * 1024:
            # policy for S1 from h1 to h3
            # 512Kbps
            print "521Kbps"
            pusher.set({
                'switch': "00:00:00:00:00:00:00:01",
                "name": "S1Limit512Kh1toh3",
                "cookie": "0",
                "priority": "32766",
                "in_port": "1",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": "set_queue=2,output=3"
            })

            # policy for S3 from h1 to h3
            # 512Kbps
            pusher.set({
                'switch': "00:00:00:00:00:00:00:03",
                "name": "S3Limit512Kh1toh3",
                "cookie": "0",
                "priority": "32766",
                "in_port": "2",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": "set_queue=2,output=1"
            })
        else:
            # policy for S1 from h1 to h3
            # drop
            print "Drop"
            pusher.set({
                'switch': "00:00:00:00:00:00:00:01",
                "name": "S1Droph1toh3",
                "cookie": "0",
                "priority": "32767",
                "in_port": "1",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": ""
            })

            # policy for S3 from h1 to h3
            # drop
            pusher.set({
                'switch': "00:00:00:00:00:00:00:03",
                "name": "S3Droph1toh3",
                "cookie": "0",
                "priority": "32767",
                "in_port": "2",
                "eth_type": "0x800",
                "ipv4_src": "10.0.0.1",
                "ipv4_dst": "10.0.0.3",
                "ip_proto": "0x06",
                "tcp_dst": "80",
                "active": "true",
                "actions": ""
            })

def checkMatch(head):
    return "eth_type" in head and head["eth_type"] == "0x0x800" \
        and "ip_proto" in head and head["ip_proto"] == "0x06" \
        and "ipv4_src" in head and head["ipv4_src"] == "10.0.0.1" \
        and "ipv4_dst" in head and head["ipv4_dst"] == "10.0.0.3" \
        and "tcp_dst" in head and head["tcp_dst"] == "80"


def staticForwarding():
    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S2->H2 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h2
    S1Staticflow1 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh2", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=2"}

    S1Staticflow2 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h2toh1", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}

    # Define static flow for Switch S2 for packet forwarding b/w h1 and h2
    S2Staticflow1 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh1", "cookie": "0", "priority": "1",
                     "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=2"}

    S2Staticflow2 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h1toh2", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}

    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S3->H3 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h3
    S1Staticflow3 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh3", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=3"}
    S1Staticflow4 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h3toh1", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h1 and h3
    S3Staticflow1 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h3toh1", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=2"}
    S3Staticflow2 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h1toh3", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=1"}

    # Below 4 flows are for setting up the static forwarding for the path H2->S2->S3->H3 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h2 and h3
    S2Staticflow3 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh3", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=3"}
    S2Staticflow4 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h3toh2", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h2 and h3
    S3Staticflow3 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h3toh2", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.3",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=3"}
    S3Staticflow4 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h2toh3", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=1"}

    # Now, Insert the flows to the switches
    pusher.set(S1Staticflow1)
    pusher.set(S1Staticflow2)
    pusher.set(S1Staticflow3)
    pusher.set(S1Staticflow4)

    pusher.set(S2Staticflow1)
    pusher.set(S2Staticflow2)
    pusher.set(S2Staticflow3)
    pusher.set(S2Staticflow4)

    pusher.set(S3Staticflow1)
    pusher.set(S3Staticflow2)
    pusher.set(S3Staticflow3)
    pusher.set(S3Staticflow4)


if __name__ == '__main__':
    staticForwarding()
    S1toS2()
    S2toS3()
    S1toS3()
    pass

#!/usr/bin/python
"""
@Student <YE JIAWEI/A0212246R>
Date : Oct 24th
"""

import httplib
import json
import Automonitor as mon
import time as t

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
    S2Staticflow1 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh1", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
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
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=4"}
    S3Staticflow2 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h1toh3", "cookie": "0",
                     "priority": "1", "in_port": "4", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
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
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=5"}
    S3Staticflow4 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h2toh3", "cookie": "0",
                     "priority": "1", "in_port": "5", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.3", "active": "true", "actions": "output=1"}

    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S3->H4 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h4
    S1Staticflow5 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh4", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.4", "active": "true", "actions": "output=3"}
    S1Staticflow6 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h4toh1", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.4",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h1 and h4
    S3Staticflow5 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h4toh1", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.4",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=4"}
    S3Staticflow6 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h1toh4", "cookie": "0",
                     "priority": "1", "in_port": "4", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.4", "active": "true", "actions": "output=2"}

    # Below 4 flows are for setting up the static forwarding for the path H2->S2->S3->H4 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h2 and h4
    S2Staticflow5 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh4", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.4", "active": "true", "actions": "output=3"}
    S2Staticflow6 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h4toh2", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.4",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h2 and h4
    S3Staticflow7 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h4toh2", "cookie": "0",
                     "priority": "1", "in_port": "2", "eth_type": "0x800", "ipv4_src": "10.0.0.4",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=5"}
    S3Staticflow8 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h2toh4", "cookie": "0",
                     "priority": "1", "in_port": "5", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.4", "active": "true", "actions": "output=2"}

    # Below 4 flows are for setting up the static forwarding for the path H1->S1->S3->H5 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h1 and h5
    S1Staticflow7 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h1toh5", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                     "ipv4_dst": "10.0.0.5", "active": "true", "actions": "output=3"}
    S1Staticflow8 = {'switch': "00:00:00:00:00:00:00:01", "name": "S1h5toh1", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.5",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h1 and h5
    S3Staticflow9 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h5toh1", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.5",
                     "ipv4_dst": "10.0.0.1", "active": "true", "actions": "output=4"}
    S3Staticflow10 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h1toh5", "cookie": "0",
                      "priority": "1", "in_port": "4", "eth_type": "0x800", "ipv4_src": "10.0.0.1",
                      "ipv4_dst": "10.0.0.5", "active": "true", "actions": "output=3"}

    # Below 4 flows are for setting up the static forwarding for the path H2->S2->S3->H5 & vice-versa
    # Define static flow for Switch S1 for packet forwarding b/w h2 and h5
    S2Staticflow7 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h2toh5", "cookie": "0",
                     "priority": "1", "in_port": "1", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                     "ipv4_dst": "10.0.0.5", "active": "true", "actions": "output=3"}
    S2Staticflow8 = {'switch': "00:00:00:00:00:00:00:02", "name": "S2h5toh2", "cookie": "0",
                     "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.5",
                     "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=1"}
    # Define static flow for Switch S3 for packet forwarding b/w h2 and h5
    S3Staticflow11 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h5toh2", "cookie": "0",
                      "priority": "1", "in_port": "3", "eth_type": "0x800", "ipv4_src": "10.0.0.5",
                      "ipv4_dst": "10.0.0.2", "active": "true", "actions": "output=5"}
    S3Staticflow12 = {'switch': "00:00:00:00:00:00:00:03", "name": "S3h2toh5", "cookie": "0",
                      "priority": "1", "in_port": "5", "eth_type": "0x800", "ipv4_src": "10.0.0.2",
                      "ipv4_dst": "10.0.0.5", "active": "true", "actions": "output=3"}

    # Now, Insert the flows to the switches
    pusher.set(S1Staticflow1)
    pusher.set(S1Staticflow2)
    pusher.set(S1Staticflow3)
    pusher.set(S1Staticflow4)
    pusher.set(S1Staticflow5)
    pusher.set(S1Staticflow6)
    pusher.set(S1Staticflow7)
    pusher.set(S1Staticflow8)

    pusher.set(S2Staticflow1)
    pusher.set(S2Staticflow2)
    pusher.set(S2Staticflow3)
    pusher.set(S2Staticflow4)
    pusher.set(S2Staticflow5)
    pusher.set(S2Staticflow6)
    pusher.set(S2Staticflow7)
    pusher.set(S2Staticflow8)

    pusher.set(S3Staticflow1)
    pusher.set(S3Staticflow2)
    pusher.set(S3Staticflow3)
    pusher.set(S3Staticflow4)
    pusher.set(S3Staticflow5)
    pusher.set(S3Staticflow6)
    pusher.set(S3Staticflow7)
    pusher.set(S3Staticflow8)
    pusher.set(S3Staticflow9)
    pusher.set(S3Staticflow10)
    pusher.set(S3Staticflow11)
    pusher.set(S3Staticflow12)

def autoRouting():
    switch = False
    while True:
        time_prev = 0
        time_after = 0
        h2toh3_byteCount_prev = 0
        h2toh3_byteCount_after = 0
        h1toh4_byteCount_prev = 0
        h1toh4_byteCount_after = 0
        h2toh5_byteCount_prev = 0
        h2toh5_byteCount_after = 0


        time_prev, h2toh3_byteCount_prev, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.2", "10.0.0.3")
        _, h1toh4_byteCount_prev, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.1", "10.0.0.4")
        _, h2toh5_byteCount_prev, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.2", "10.0.0.5")


        t.sleep(1)

        time_after, h2toh3_byteCount_after, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.2", "10.0.0.3")
        _, h1toh4_byteCount_after, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.1", "10.0.0.4")
        _, h2toh5_byteCount_after, _ = mon.getStatics("00:00:00:00:00:00:00:03", "10.0.0.2", "10.0.0.5")   

        time = time_after - time_prev
        byteCount = h2toh3_byteCount_after - h2toh3_byteCount_prev + h1toh4_byteCount_after - h1toh4_byteCount_prev + h2toh5_byteCount_after - h2toh5_byteCount_prev

        if (time == 0):
            print("error! difference between two time stamps obtained from mointor is 0!")
            break

        tp = byteCount * 8.0 / 1000000 / time
        print "time duration: ", time
        print "h2 tp h3 throughput: ", (h2toh3_byteCount_after - h2toh3_byteCount_prev)*8.0/1000000, "Mbps"
        print "h1 tp h4 throughput: ", (h1toh4_byteCount_after - h1toh4_byteCount_prev)*8.0/1000000, "Mbps"
        print "h2 tp h5 throughput: ", (h2toh5_byteCount_after - h2toh5_byteCount_prev)*8.0/1000000, "Mbps"
        print "total tp: ", tp

        tp = (h2toh3_byteCount_after - h2toh3_byteCount_prev + h2toh5_byteCount_after - h2toh5_byteCount_prev) * 8.0 / 1000000 / time
        print "link between s2 and s3 tp: ", tp

        if (not switch and tp > 90):
            print "switch route"
            reroute()
            switch = True


def reroute():
    print 'switching to H2 -> S2 -> S1 -> S3 -> H5'

    myflow1 = {
        'switch': "00:00:00:00:00:00:00:01",
        "name": "Alt_S1_h2toh5", "cookie": "0",
        "priority": "100",
        "eth_type": "0x0800",
        "ipv4_src": "10.0.0.2", "ipv4_dst": "10.0.0.5",
        "active": "true",
        "in_port": "2",
        "actions": "output=3"
    }
    pusher.set(myflow1)

    myflow2 = {
        'switch': "00:00:00:00:00:00:00:02",
        "name": "Alt_S2_h2toh5", "cookie": "0",
        "priority": "100",
        "eth_type": "0x0800",
        "ipv4_src": "10.0.0.2", "ipv4_dst": "10.0.0.5",
        "active": "true",
        "in_port": "1",
        "actions": "output=2"
    }
    pusher.set(myflow2)

    myflow3 = {
        'switch': "00:00:00:00:00:00:00:03",
        "name": "Alt_S3_h2toh5", "cookie": "0",
        "priority": "100",
        "eth_type": "0x0800",
        "ipv4_src": "10.0.0.2", "ipv4_dst": "10.0.0.5",
        "active": "true",
        "in_port": "4",
        "actions": "output=3"
    }
    pusher.set(myflow3)



if __name__ == '__main__':
    staticForwarding()
    autoRouting()
    pass
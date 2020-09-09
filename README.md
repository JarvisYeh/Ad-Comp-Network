@Author <YE JIAWEI/A0212246R>
Date : 09/09/2020


####################################################
## Policy 1
####################################################
### Requirements:
Communication between H2 to H3 and vice-versa:
Block all traffic using destination UDP ports from 1000 - 1100.

### Idea:
Add policy for both S2 and S3.
With the help of for loop, iterate through 1000 - 1100.
One for loop set rules for S2 targeting those udp_dst=1000 to 1100 with no action value perform (e.g. drop).
One for loop set rules for S3 targeting those udp_dst=1000 to 1100 with no action value perform (e.g. drop).
Note that using upd_dst key need prerequisite ip_proto = 0x11
Also set priority to default maximum: 32767 so that new rules could overwrite static flow rules.

### Logs:
#### Communication from H2 to H3:
##### Port 999:
###### Host 2:
```
Connecting to host 10.0.0.3, port 999
[ 20] local 10.0.0.2 port 42553 connected to 10.0.0.3 port 999
[ ID] Interval           Transfer     Bandwidth       Total Datagrams
[ 20]   0.00-1.00   sec   120 KBytes   983 Kbits/sec  15  
[ 20]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  16  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 20]   0.00-10.00  sec  1.24 MBytes  1.04 Mbits/sec  0.082 ms  0/159 (0%)  
[ 20] Sent 159 datagrams

iperf Done.
```
UDP packet transfer from h2 to h3 port 999 is not blocked, therefore, the bandwidth here is 1.03Mbps.


###### Host 3
```
-----------------------------------------------------------
Server listening on 999
-----------------------------------------------------------
Accepted connection from 10.0.0.2, port 48774
[ 21] local 10.0.0.3 port 999 connected to 10.0.0.2 port 42553
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-1.00   sec   120 KBytes   983 Kbits/sec  0.040 ms  0/15 (0%)  
[ 21]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  0.050 ms  0/16 (0%)  
[ 21]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  0.071 ms  0/16 (0%)  
[ 21]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  0.122 ms  0/16 (0%)  
[ 21]   4.00-5.01   sec   128 KBytes  1.04 Mbits/sec  0.119 ms  0/16 (0%)  
[ 21]   5.01-6.00   sec   128 KBytes  1.05 Mbits/sec  0.101 ms  0/16 (0%)  
[ 21]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  0.103 ms  0/16 (0%)  
[ 21]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  0.067 ms  0/16 (0%)  
[ 21]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  0.127 ms  0/16 (0%)  
[ 21]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  0.082 ms  0/16 (0%)  
[ 21]  10.00-10.04  sec  0.00 Bytes  0.00 bits/sec  0.082 ms  0/0 (-nan%)  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-10.04  sec  1.24 MBytes  1.04 Mbits/sec  0.082 ms  0/159 (0%)  
-----------------------------------------------------------
Server listening on 999
-----------------------------------------------------------
```
Host 3 as server could hear the UDP packet from port 999.

#### Port 1000
###### Host 2
```
Connecting to host 10.0.0.3, port 1000
> iperf3: error - unable to read from stream socket: Resource temporarily unavailable.
```
UDP packet transfer from h2 to h3 port 1000 is blocked, therefore, the there is no response from server. Switch drop the packet directly.

###### Host 3
```
-----------------------------------------------------------
Server listening on 1000
-----------------------------------------------------------
Accepted connection from 10.0.0.2, port 53192
>iperf3: the client has unexpectedly closed the connections
-----------------------------------------------------------
Server listening on 1000
-----------------------------------------------------------
```
Host 3 as server could not hear the UDP packet from port 1000 since it's been dropped by switch.

#### Port 1100
###### Host 2
```
Connecting to host 10.0.0.3, port 1100
>iperf3: the client has unexpectedly closed the connections
```
UDP packet transfer from h2 to h3 port 1100 is blocked, therefore, the there is no response from server. Switch drop the packet directly.

###### Host 3
```
-----------------------------------------------------------
Server listening on 1100
-----------------------------------------------------------
Accepted connection from 10.0.0.2, port 57136
>iperf3: the client has unexpectedly closed the connections
-----------------------------------------------------------
Server listening on 1100
-----------------------------------------------------------
```
Host 3 as server could not hear the UDP packet from port 1100 since it's been dropped by switch.

#### Port 1101
###### Host 2
```
Connecting to host 10.0.0.3, port 1101
[ 20] local 10.0.0.2 port 53363 connected to 10.0.0.3 port 1101
[ ID] Interval           Transfer     Bandwidth       Total Datagrams
[ 20]   0.00-1.00   sec   120 KBytes   982 Kbits/sec  15  
[ 20]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  16  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 20]   0.00-10.00  sec  1.24 MBytes  1.04 Mbits/sec  0.088 ms  0/159 (0%)  
[ 20] Sent 159 datagrams

iperf Done.
```
UDP packet transfer from h2 to h3 port 1101 is not blocked, therefore, the bandwidth here is 1.04Mbps.

###### Host 3
```
-----------------------------------------------------------
Server listening on 1101
-----------------------------------------------------------
Accepted connection from 10.0.0.2, port 51604
[ 21] local 10.0.0.3 port 1101 connected to 10.0.0.2 port 53363
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-1.00   sec   120 KBytes   982 Kbits/sec  0.046 ms  0/15 (0%)  
[ 21]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  0.052 ms  0/16 (0%)  
[ 21]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  0.080 ms  0/16 (0%)  
[ 21]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  0.100 ms  0/16 (0%)  
[ 21]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  0.088 ms  0/16 (0%)  
[ 21]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  0.081 ms  0/16 (0%)  
[ 21]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  0.076 ms  0/16 (0%)  
[ 21]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  0.077 ms  0/16 (0%)  
[ 21]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  0.086 ms  0/16 (0%)  
[ 21]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  0.088 ms  0/16 (0%)  
[ 21]  10.00-10.04  sec  0.00 Bytes  0.00 bits/sec  0.088 ms  0/0 (-nan%)  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-10.04  sec  1.24 MBytes  1.04 Mbits/sec  0.088 ms  0/159 (0%)  
-----------------------------------------------------------
Server listening on 1101
-----------------------------------------------------------
```
Host 3 as server could hear the UDP packet from port 1101.

#### Communication from H3 to H2
##### Port 999
###### Host 2
```
-----------------------------------------------------------
Server listening on 999
-----------------------------------------------------------
Accepted connection from 10.0.0.3, port 35114
[ 21] local 10.0.0.2 port 999 connected to 10.0.0.3 port 48451
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-1.00   sec   120 KBytes   982 Kbits/sec  0.044 ms  0/15 (0%)  
[ 21]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  0.095 ms  0/16 (0%)  
[ 21]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  0.336 ms  0/16 (0%)  
[ 21]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  0.164 ms  0/16 (0%)  
[ 21]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  0.137 ms  0/16 (0%)  
[ 21]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  0.109 ms  0/16 (0%)  
[ 21]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  0.118 ms  0/16 (0%)  
[ 21]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  0.119 ms  0/16 (0%)  
[ 21]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  0.110 ms  0/16 (0%)  
[ 21]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  0.112 ms  0/16 (0%)  
[ 21]  10.00-10.04  sec  0.00 Bytes  0.00 bits/sec  0.112 ms  0/0 (-nan%)  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-10.04  sec  1.24 MBytes  1.04 Mbits/sec  0.112 ms  0/159 (0%)  
-----------------------------------------------------------
Server listening on 999
-----------------------------------------------------------
```
Host 2 as server could hear the UDP packet from port 1101.

###### Host 3
```
Connecting to host 10.0.0.2, port 999
[ 20] local 10.0.0.3 port 48451 connected to 10.0.0.2 port 999
[ ID] Interval           Transfer     Bandwidth       Total Datagrams
[ 20]   0.00-1.00   sec   120 KBytes   983 Kbits/sec  15  
[ 20]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  16  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 20]   0.00-10.00  sec  1.24 MBytes  1.04 Mbits/sec  0.112 ms  0/159 (0%)  
[ 20] Sent 159 datagrams

iperf Done.
```
UDP packet transfer from h3 to h2 port 999 is not blocked, therefore, the bandwidth here is 1.04Mbps.

#### Port 1000
###### Host 2
```
-----------------------------------------------------------
Server listening on 1000
-----------------------------------------------------------
Accepted connection from 10.0.0.3, port 38238
>iperf3: the client has unexpectedly closed the connections
-----------------------------------------------------------
Server listening on 1000
-----------------------------------------------------------
```
Host 2 as server could not hear the UDP packet from port 1000 since it's been dropped by switch.

###### Host 3
```
Connecting to host 10.0.0.2, port 1000
iperf3: error - unable to read from stream socket: Resource temporarily unavailable.
```
UDP packet transfer from h3 to h2 port 1000 is blocked, therefore, the there is no response from server. Switch drop the packet directly.

#### Port 1100
###### Host 2
```
-----------------------------------------------------------
Server listening on 1100
-----------------------------------------------------------
Accepted connection from 10.0.0.3, port 33316
iperf3: the client has unexpectedly closed the connections
-----------------------------------------------------------
Server listening on 1100
-----------------------------------------------------------
```
Host 2 as server could not hear the UDP packet from port 1100 since it's been dropped by switch.

###### Host 3
```
Connecting to host 10.0.0.2, port 1100
iperf3: error - unable to read from stream socket: Resource temporarily unavailable.
```
UDP packet transfer from h3 to h2 port 1100 is blocked, therefore, the there is no response from server. Switch drop the packet directly.

#### Port 1101
###### Host 2
```
-----------------------------------------------------------
Server listening on 1101
-----------------------------------------------------------
Accepted connection from 10.0.0.3, port 42670
[ 21] local 10.0.0.2 port 1101 connected to 10.0.0.3 port 53141
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-1.00   sec   120 KBytes   982 Kbits/sec  0.044 ms  0/15 (0%)  
[ 21]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  0.044 ms  0/16 (0%)  
[ 21]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  0.059 ms  0/16 (0%)  
[ 21]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  0.063 ms  0/16 (0%)  
[ 21]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  0.097 ms  0/16 (0%)  
[ 21]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  0.397 ms  0/16 (0%)  
[ 21]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  0.203 ms  0/16 (0%)  
[ 21]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  0.375 ms  0/16 (0%)  
[ 21]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  0.178 ms  0/16 (0%)  
[ 21]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  0.099 ms  0/16 (0%)  
[ 21]  10.00-10.04  sec  0.00 Bytes  0.00 bits/sec  0.099 ms  0/0 (-nan%)  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 21]   0.00-10.04  sec  1.24 MBytes  1.04 Mbits/sec  0.099 ms  0/159 (0%)  
-----------------------------------------------------------
Server listening on 1101
-----------------------------------------------------------
```
Host 2 as server could hear the UDP packet from port 1101.

###### Host 3
```
Connecting to host 10.0.0.2, port 1101
[ 20] local 10.0.0.3 port 53141 connected to 10.0.0.2 port 1101
[ ID] Interval           Transfer     Bandwidth       Total Datagrams
[ 20]   0.00-1.00   sec   120 KBytes   983 Kbits/sec  15  
[ 20]   1.00-2.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   2.00-3.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   3.00-4.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   4.00-5.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   5.00-6.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   6.00-7.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   7.00-8.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   8.00-9.00   sec   128 KBytes  1.05 Mbits/sec  16  
[ 20]   9.00-10.00  sec   128 KBytes  1.05 Mbits/sec  16  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Jitter    Lost/Total Datagrams
[ 20]   0.00-10.00  sec  1.24 MBytes  1.04 Mbits/sec  0.099 ms  0/159 (0%)  
[ 20] Sent 159 datagrams

iperf Done.
```
UDP packet transfer from h3 to h2 port 1101 is not blocked, therefore, the bandwidth here is 1.04Mbps.


####################################################
## Policy 2
####################################################
### Requirements:
Communication from H1 to H2:
Rate limit traffic to 1 Mbps.

### Idea:
Add policy for both S1 and S2.
Add actom set_queue=1 so that use mininet_add_queue queue 1, which has the rate limit of 1Mbps.
Also set priority to default maximum: 32767 so that new rules could overwrite static flow rules.

### Logs:
#### Communication from H1 to H2:
###### Host 2
```
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
Accepted connection from 10.0.0.1, port 42664
[ 21] local 10.0.0.2 port 5201 connected to 10.0.0.1 port 42666
[ ID] Interval           Transfer     Bandwidth
[ 21]   0.00-1.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   1.00-2.00   sec   116 KBytes   949 Kbits/sec                  
[ 21]   2.00-3.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   3.00-4.00   sec   119 KBytes   973 Kbits/sec                  
[ 21]   4.00-5.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   5.00-6.00   sec   117 KBytes   961 Kbits/sec                  
[ 21]   6.00-7.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   7.00-8.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   8.00-9.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   9.00-10.00  sec   119 KBytes   974 Kbits/sec                  
[ 21]  10.00-11.00  sec   116 KBytes   950 Kbits/sec                  
[ 21]  11.00-12.00  sec   116 KBytes   950 Kbits/sec                  
[ 21]  12.00-13.00  sec   117 KBytes   962 Kbits/sec                  
[ 21]  13.00-13.01  sec  0.00 Bytes  0.00 bits/sec                  
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[ 21]   0.00-13.01  sec  2.55 MBytes  1.65 Mbits/sec    0             sender
[ 21]   0.00-13.01  sec  1.48 MBytes   955 Kbits/sec                  receiver
-----------------------------------------------------------
Server listening on 5201
-----------------------------------------------------------
```
Host 2 as receiver has the average bandwith = 955Kbps, which is less than 1Mbps.

####################################################
## Policy 3
####################################################
### Requirements:
Communication from H1 to H3: (15 points) Regulate HTTP traffic using the below logic:
* When the total transfer is less than 20Mb, rate limit Traffic to 1Mbps.
* If total transfer is between 20Mb to 30Mb, rate limit to 512Kbps.
* If total transfer is more than 30Mb, drop packets.


### Idea:
Initialize a total_bit variable to 0.
While the total_bit is less than 30Mb, keep:
* Send http request to switch 1 accquires the for the flows inforamtion go through it.
* Check if flows contains the target http flow (e.g. tcp request, destination port = 80).
* If there is, obtain the value of "byteCount" from the response, and set total_bit = flow[byteCount] * 8.
* Determine which policy to set based on total_bit with the help of condition logic. There are three sepereate policy.
  * action=set_queue=1, which means 1MBps
  * action=set_queue=2, which means 512Kbps
  * action="", which means drop the packet 

### Logs:
```
-----------------------------------------------------------
Server listening on 80
-----------------------------------------------------------
Accepted connection from 10.0.0.1, port 60300
[ 21] local 10.0.0.3 port 80 connected to 10.0.0.1 port 60354
[ ID] Interval           Transfer     Bandwidth
[ 21]   0.00-1.00   sec   116 KBytes   949 Kbits/sec                  
[ 21]   1.00-2.00   sec   116 KBytes   951 Kbits/sec                  
[ 21]   2.00-3.00   sec   116 KBytes   950 Kbits/sec                  
[ 21]   3.00-4.00   sec   119 KBytes   973 Kbits/sec  
...    
```
Initial bandwidth has upper limit 1Mbps.

```
...
[ 21]  22.00-23.00  sec  59.4 KBytes   487 Kbits/sec                  
[ 21]  23.00-24.00  sec  60.8 KBytes   498 Kbits/sec                  
[ 21]  24.00-25.00  sec  59.4 KBytes   486 Kbits/sec                  
[ 21]  25.00-26.00  sec  59.4 KBytes   487 Kbits/sec                  
[ 21]  26.00-27.00  sec  60.8 KBytes   498 Kbits/sec                  
[ 21]  27.00-28.00  sec  59.4 KBytes   486 Kbits/sec
...
```
After about 20 sec bandwidth has upper limit 512Kbps.

```
...
[ 21]  66.00-67.00  sec  0.00 Bytes  0.00 bits/sec                  
[ 21]  67.00-68.00  sec  0.00 Bytes  0.00 bits/sec                  
[ 21]  68.00-69.00  sec  0.00 Bytes  0.00 bits/sec                  
[ 21]  69.00-70.00  sec  0.00 Bytes  0.00 bits/sec                  
[ 21]  70.00-71.00  sec  0.00 Bytes  0.00 bits/sec                  
[ 21]  71.00-72.00  sec  0.00 Bytes  0.00 bits/sec
...
```
After about 65 sec, the packets are dropped by switches and will not received by host 3.
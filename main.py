import struct
import sys

from udpEngine import transOICQNum
from udpEngine import udpEngineRun
from udpEngine import udpPretreatment
from udpEngine import udpPendingAnalysis
from tcpEngine import tcpEngineRun
from tcpEngine import marketBasketAnalysis
from initConfigure import readConfigure
from aprioriGen import *
from fileOp import writeUdpPacketStreamData

import threading
from time import sleep, ctime, time

sysLen = len(sys.argv)

path = 'Data/TD/'

fpcap = open(path+'xuan1.cap', 'rb')
fTCPtxt = open(path+'tcp.txt', 'wb')
fUDPtxt = open(path+'udp.txt', 'wb')
fTCPloadtxt = open(path+'tcpload.txt', 'wb')
fUDPloadtxt = open(path+'udpload.txt', 'wb')

stringData = fpcap.read()

tcpPacketStreamBase = []
tcpPacketStreamData = []

udpPacketStreamBase = []
udpPacketStreamData = []
udpTestedPacketStreamData = []

udpTestedPacketStreamData.append([])
udpTestedPacketStreamData.append([])
udpTestedPacketStreamData.append([])

# pcap header analysis
pcapHeader = {}
pcapHeader['magic_number'] = stringData[0:4]
pcapHeader['version_major'] = stringData[4:6]
pcapHeader['version_minor'] = stringData[6:8]
pcapHeader['thiszone'] = stringData[8:12]
pcapHeader['sigfigs'] = stringData[12:16]
pcapHeader['snaplen'] = stringData[16:20]
pcapHeader['linktype'] = stringData[20:24]

attrMBThreshold, attrMBSYN = readConfigure()

# transform pcap header into result.txt
#ftxt.write("Pcap Header:\n")
#for key in ['magic_number','version_major','version_minor',
#		'thiszone','sigfigs','snaplen','linktype']:
#	ftxt.write(key+" : "+repr(pcapHeader[key])+'\n')
#ftxt.write('\n')

# pcap packet analysis
step = 0
packetNum = 0
packetData = []
packetInfo = {}
pcapPacketHeader = {}
stringDataLen = len(stringData)
i = 24
while (i < stringDataLen):
	pcapPacketHeader['GMTtime'] = stringData[i:i+4]
	pcapPacketHeader['MicroTime'] = stringData[i+4:i+8]
	pcapPacketHeader['caplen'] = stringData[i+8:i+12]
	pcapPacketHeader['len'] = stringData[i+12:i+16]
	# cal len
	packetLen = struct.unpack('I',pcapPacketHeader['caplen'])[0]
	# write this packet
	packetData.append(stringData[i+16:i+16+packetLen])
	# final analysis
	i = i+packetLen+16
	packetNum += 1

# write data info on result.txt
i = 0
while i < packetNum:
	# write header
#	ftxt.write("This is number "+str(i)+" packet:"+"\n")
#	for key in ['GMTtime','MicroTime','caplen','len']:
#		ftxt.write(key+" : "+repr(pcapPacketHeader[key])+"\n")
	# write data
	packetInfo['srcMac'] = packetData[i][:6]
	packetInfo['desMac'] = packetData[i][6:12]
	packetInfo['type'] = packetData[i][12:14]
	if '\x08\x00' == packetInfo['type']:
		packetInfo['protocol'] = packetData[i][23]
		packetInfo['srcIP'] = packetData[i][26:30]
		packetInfo['desIP'] = packetData[i][30:34]
		packetInfo['srcPort'] = packetData[i][34:36]
		packetInfo['desPort'] = packetData[i][36:38]
		# UDP
		if '\x11' == packetInfo['protocol']:
			udpLen = ord(packetData[i][38])*16*16+ord(packetData[i][39])
			packetInfo['payload'] = packetData[i][42:42+udpLen]
			fUDPtxt.write(packetInfo['srcIP']
				+ packetInfo['desIP']
				+ packetInfo['srcPort']
				+ packetInfo['desPort']
				+ packetInfo['payload']
				)
			fUDPtxt.write("|#|")
			udpPacketStreamBase, udpPacketStreamData, udpTestedPacketStreamData =  udpEngineRun(udpPacketStreamBase, udpPacketStreamData, packetInfo, udpTestedPacketStreamData)
		# TCP
		elif '\x06' == packetInfo['protocol']:
			pass
			packetInfo['flag'] = packetData[i][47]
			tcpLength = len(packetData[i])
			unit = tcpLength%16
			decade = ((tcpLength-unit)/16)%16
			hundred = tcpLength/16/16
			packetInfo['length'] = chr(hundred)+chr(decade)+chr(unit)
			packetInfo['payload'] = packetData[i][54:]
			fTCPtxt.write(packetInfo['srcIP']
				+ packetInfo['desIP']
				+ packetInfo['srcPort']
				+ packetInfo['desPort']
				+ packetInfo['length']
				+ packetInfo['flag']
				+ packetInfo['payload']
				)
			fTCPtxt.write("|#|")
			tcpPacketStreamBase, tcpPacketStreamData = tcpEngineRun(tcpPacketStreamBase, tcpPacketStreamData, packetInfo)
		# ICMP
		elif '\x01' == packetInfo['protocol']:
			pass
#			print "ICMP"
#	ftxt.write("Packet data:"+repr(packetData[i])+'\r\n\r\n')
	i += 1
# SMail Test process
#sMailProcessing(tcpPacketStreamData)

# ================== TCP ========================
# marketBasketAnalysis Test Process
#marketBasketAnalysis(attrMBThreshold, attrMBSYN)

# ================== UDP ========================
for index in range(sysLen):
	if sys.argv[index] == '-upre' or sys.argv[index] == '-all':
		# udp.txt --> udpStatistic.txt
		udpPretreatment('udp.txt', 'udpStatistic')
		udpPendingAnalysis()
for index in range(sysLen):
	if sys.argv[index] == '-uapr' or sys.argv[index] == '-all':
		# UDP Apriori: udpPacketStreamData --> udpStream.txt
		writeUdpPacketStreamData(udpPacketStreamData)
		dataSet = udpAprioriGen()

		ansSet = []
		threshold = 0.6
		frontLen = 2
		aprioriFactory(dataSet, udpPacketStreamData)
		fans = open(path+'apriori.txt', 'w')
		while threshold < 1.00:
			frontLen = 2
			while frontLen < 1024:
				startTime = time()
				revL = aprioriFactory(dataSet, udpPacketStreamData, threshold, frontLen)
				endTime = time()
				gapTime = endTime - startTime
				fans.write("%d %.4lf %.4lf %r\n" % (frontLen, threshold, gapTime, revL))
				frontLen += 1
			threshold += 0.01
			print threshold
		fans.close()
		print "....................................."
	
		ansSet = []
		threshold = 0.6
		frontLen = 2
# standardL need to be updated by person
#		standardL = aprioriFactory(dataSet, udpTestedPacketStreamData, 0.9, 12)
		fansed = open(path+'aprioried.txt', 'w')
		while threshold < 1.00:
			frontLen = 2
			while frontLen < 1024:
				startTime = time()
				revL = aprioriFactory(dataSet, udpTestedPacketStreamData, threshold, frontLen)
				endTime = time()
				gapTime = endTime - startTime
				fansed.write("%d %.4lf %.4lf %r\n" % (frontLen, threshold, gapTime, revL))
				frontLen += 1
			threshold += 0.01
			print threshold
		fansed.close()

# ===============================================
for index in range(sysLen):
	if sys.argv[index] == '-uload' or sys.argv[index] == 'all':
		pktStreamLen = len(udpPacketStreamData)
		for i in range(pktStreamLen):
			fUDPloadtxt.write(repr(udpPacketStreamData))

# ===============================================
for index in range(sysLen):
	if sys.argv[index] == '-tload' or sys.argv[index] == '-all':
		pktStreamLen = len(tcpPacketStreamData)
		for i in range(pktStreamLen):
			fTCPloadtxt.write(repr(tcpPacketStreamData[i]))

#ftxt.write("Total "+str(packetNum)+" packet"+'\r\n')

fUDPtxt.close()
fTCPtxt.close()
fpcap.close()


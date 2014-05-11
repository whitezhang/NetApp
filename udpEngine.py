from fileOp import writeFile
from fileOp import writeStatisticFile

from transEngine import ipTrans
from transEngine import portTrans

def transOICQNum(number):
	qNumber = 0
	for i in range(4):
		qNumber += 16**(2*i)*ord(number[3-i])
	return qNumber

def udpPretreatment(srcFileName, desFileName):
	path = 'Data/TD/'
	fName = path+srcFileName
	ftxt = open(fName, 'rb')
	try:
		line = ftxt.read().split("|#|")
		lineLen = len(line)
	except IOError, e:
		print "No file name"
	else:
# streamInfo is used to dealing with the current packet info

# streamMapData is used to store correlation info:
#	srcIP, srcPort,
#	number of bytes(rbyte/pbyte),
#	number of packets in request/response(rpack/ppack),
#	size of first data packet payload(rhbyte1/phbyte1),
#	size of second data packet payload(rhbyte2/phbyte2),
#	details of packets in request/response(rbytes/pbytes),

#	average packet size(ravgbyte/pavgbyte)
#	mean square deviation in request/response(rmsd/pmsd)

# streamMapData current version:
# 	0: srcIP
# 	1: srcPort
# 	2: rbyte
# 	3: pbyte
# 	4: rhbyte1
# 	5: rsizesum
# 	6: psizesum
#	7: rbytes
#	8: pbytes
#	9: desIP
#	10: desPort
		streamInfo = {}
		streamMapData = []
		streamLen = 0
		k = 0
		while k < lineLen:
			streamInfo['srcIP'] = line[k][0:4]
			streamInfo['desIP'] = line[k][4:8]
			streamInfo['srcPort'] = line[k][8:10]
			streamInfo['desPort'] = line[k][10:12]
			streamInfo['payload'] = line[k][12:]
			streamInfo['len'] = len(streamInfo['payload'])+42

			srcMap = []
			srcMap.append(streamInfo['srcIP'])
			srcMap.append(streamInfo['srcPort'])
			desMap = []
			desMap.append(streamInfo['desIP'])
			desMap.append(streamInfo['desPort'])

			flag = 0
			i = 0
			while i < streamLen:
				if not cmp(srcMap[0], streamMapData[i][0]) and not cmp(srcMap[1], streamMapData[i][1]) \
					and not cmp(desMap[0], streamMapData[i][9]) and not cmp(desMap[1], streamMapData[i][10]):
					break
				i += 1
			if i == streamLen:
				flag = 1
			else:
# This part is to calculate the number of packets in request
				streamMapData[i][9] = streamInfo['desIP']
				streamMapData[i][10] = streamInfo['desPort']
				streamMapData[i][2] += 1
				streamMapData[i][5] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][7].extend(tmp)
				k += 1
				continue	
#			print srcMap
#			print desMap
#			print streamMapData
			i = 0
			while i < streamLen:
				if not cmp(desMap[0], streamMapData[i][0]) and not cmp(desMap[1], streamMapData[i][1]) \
					and not cmp(srcMap[0], streamMapData[i][9]) and not cmp(srcMap[1], streamMapData[i][10]):
					break
				i += 1
			if i == streamLen and 1 == flag:
# Position two and three denote rpack and ppack
				srcMap.append(1)
				srcMap.append(0)
				srcMap.append(streamInfo['len'])
				srcMap.append(streamInfo['len'])
				srcMap.append(0)
				tmp = []
				tmp.append(streamInfo['len'])
				srcMap.append(tmp)
				srcMap.append([])
				srcMap.append(streamInfo['desIP'])
				srcMap.append(streamInfo['desPort'])
				streamLen += 1
				streamMapData.append(srcMap)
			else:
# This part is to calculate the number of packets in response
				streamMapData[i][9] = streamInfo['srcIP']
				streamMapData[i][10] = streamInfo['srcPort']
				streamMapData[i][3] += 1
				streamMapData[i][6] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][8].extend(tmp)
			k += 1
	finally:
		ftxt.close()
		writeStatisticFile(streamMapData, streamLen, desFileName)


def udpPendingAnalysis():
	path = 'Data/TD/'
	fName = path+'udpPending.txt'
	ftxt = open(fName, 'rb')
	try:
		line = ftxt.read().split("|#|")
		lineLen = len(line)
	except IOError, e:
		print "udpPending Error"
	else:
# streamInfo is used to dealing with the current packet info

# streamMapData is used to store correlation info:
#	srcIP, srcPort,
#	number of bytes(rbyte/pbyte),
#	number of packets in request/response(rpack/ppack),
#	size of first data packet payload(rhbyte1/phbyte1),
#	size of second data packet payload(rhbyte2/phbyte2),
#	details of packets in request/response(rbytes/pbytes),

#	average packet size(ravgbyte/pavgbyte)
#	mean square deviation in request/response(rmsd/pmsd)

# streamMapData current version:
# 	0: srcIP
# 	1: srcPort
# 	2: rbyte
# 	3: pbyte
# 	4: rhbyte1
# 	5: rsizesum
# 	6: psizesum
#	7: rbytes
#	8: pbytes
#	9: desIP
#	10: desPort
		streamInfo = {}
		streamMapData = []
		streamLen = 0
		k = 0
		while k < lineLen:
			streamInfo['srcIP'] = line[k][0:4]
			streamInfo['desIP'] = line[k][4:8]
			streamInfo['srcPort'] = line[k][8:10]
			streamInfo['desPort'] = line[k][10:12]
			streamInfo['payload'] = line[k][12:]
			streamInfo['len'] = len(streamInfo['payload'])+42

			srcMap = []
			srcMap.append(streamInfo['srcIP'])
			srcMap.append(streamInfo['srcPort'])
			desMap = []
			desMap.append(streamInfo['desIP'])
			desMap.append(streamInfo['desPort'])

			flag = 0
			i = 0
			while i < streamLen:
				if not cmp(srcMap[0], streamMapData[i][0]) and not cmp(srcMap[1], streamMapData[i][1]) \
					and not cmp(desMap[0], streamMapData[i][9]) and not cmp(desMap[1], streamMapData[i][10]):
					break
				i += 1
			if i == streamLen:
				flag = 1
			else:
# This part is to calculate the number of packets in request
				streamMapData[i][9] = streamInfo['desIP']
				streamMapData[i][10] = streamInfo['desPort']
				streamMapData[i][2] += 1
				streamMapData[i][5] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][7].extend(tmp)
				k += 1
				continue	
#			print srcMap
#			print desMap
#			print streamMapData
			i = 0
			while i < streamLen:
				if not cmp(desMap[0], streamMapData[i][0]) and not cmp(desMap[1], streamMapData[i][1]) \
					and not cmp(srcMap[0], streamMapData[i][9]) and not cmp(srcMap[1], streamMapData[i][10]):
					break
				i += 1
			if i == streamLen and 1 == flag:
# Position two and three denote rpack and ppack
				srcMap.append(1)
				srcMap.append(0)
				srcMap.append(streamInfo['len'])
				srcMap.append(streamInfo['len'])
				srcMap.append(0)
				tmp = []
				tmp.append(streamInfo['len'])
				srcMap.append(tmp)
				srcMap.append([])
				srcMap.append(streamInfo['desIP'])
				srcMap.append(streamInfo['desPort'])
				streamLen += 1
				streamMapData.append(srcMap)
			else:
# This part is to calculate the number of packets in response
				streamMapData[i][9] = streamInfo['srcIP']
				streamMapData[i][10] = streamInfo['srcPort']
				streamMapData[i][3] += 1
				streamMapData[i][6] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][8].extend(tmp)
			k += 1
	finally:
		ftxt.close()
		writeStatisticFile(streamMapData, streamLen, 'udpPendingStatistic')	

# packetInfo = ['srcIP', 'desIP', 'srcPort', 'desPort', 'payload']
# packetStreamData = [[payload11, payload12,.....], [payload21...], .....]
def udpEngineRun(packetStreamBase, packetStreamData, packetInfo, testedPacketStreamData):
#	if len(packetInfo['payload'][0]) != 0 and '\x02' == packetInfo['payload'][0]:
#		qNumber = transOICQNum(packetInfo['payload'][7:11])
#		testedPacketStreamData[0].append(packetInfo['payload'])
#		print 'OICQ %d' % qNumber
#	elif len(packetInfo['payload'][0]) != 0 and '\xe4' == packetInfo['payload'][0]:
#		testedPacketStreamData[1].append(packetInfo['payload'])
#		pass
#		print 'eDonkey'
#	elif len(packetInfo['payload'][0]) != 0 and '\xfe' == packetInfo['payload'][0]:
#		testedPacketStreamData[2].append(packetInfo['payload'])
#		pass
#		print 'BT(Old Version)'
#	elif len(packetInfo['payload'][0]) != 0 and '\x29' == packetInfo['payload'][0]:
#		pass
#	else:
#	writeFile(packetInfo, 'udpPending')

	curStream = []
	packetPort = []
	curStream.append(packetInfo['srcIP'])
	curStream.append(packetInfo['desIP'])
	unsortStream = curStream
	curStream = sorted(curStream)
	if unsortStream != curStream:
		curStream.append(1)
	else:
		curStream.append(0)
	packetPort.append(packetInfo['srcPort'])
	packetPort.append(packetInfo['desPort'])
	packetPort.sort()
	curStream.append(packetPort[0])
	curStream.append(packetPort[1])
	pktLen = len(packetStreamBase)
	i = 0
	while i < pktLen:
		if not cmp(packetStreamBase[i], curStream):
			packetStreamData[i].append(packetInfo['payload'])
			break
		i += 1
	if i == pktLen:
		packetStreamBase.append(curStream)
		tmpData = []
		tmpData.append(packetInfo['payload'])
		packetStreamData.append(tmpData)
	return packetStreamBase, packetStreamData, testedPacketStreamData

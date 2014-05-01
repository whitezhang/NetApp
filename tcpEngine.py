from transEngine import ipTrans
from transEngine import portTrans

def marketBasketAnalysis(attrMBThreshold, attrMBSYN):
	path = 'Data/TD/'
	fName = path+'tcp.txt'
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
#	7: synnum
#	8: rbytes
#	9: pbytes
#	10: desIP
#	11: desPort

# Statistics
# 	0: rpsizesum
		streamInfo = {}
		streamMapData = []
		streamLen = 0
		rpsizesum = 0
		k = 0
		while k < lineLen:
			streamInfo['srcIP'] = line[k][0:4]
			streamInfo['desIP'] = line[k][4:8]
			streamInfo['srcPort'] = line[k][8:10]
			streamInfo['desPort'] = line[k][10:12]
			hundred = ord(line[k][12])
			decade = ord(line[k][13])
			unit = ord(line[k][14])		
			streamInfo['flag'] = line[k][15]
			streamInfo['len'] = hundred*16*16+decade*16+unit
			streamInfo['payload'] = line[k][15:streamInfo['len']-54]

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
					and not cmp(desMap[0], streamMapData[i][10]) and not cmp(desMap[1], streamMapData[i][11]):
					break
				i += 1
			if i == streamLen:
				flag = 1
			else:
# This part is to calculate the number of packets in request
				streamMapData[i][10] = streamInfo['desIP']
				streamMapData[i][11] = streamInfo['desPort']
				streamMapData[i][2] += 1
				streamMapData[i][5] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][8].extend(tmp)
				rpsizesum += streamInfo['len']
				if 1 == (ord(streamInfo['flag']) & 0x01):
					streamMapData[i][7] += 1
				k += 1
				continue
			
#			print srcMap
#			print desMap
#			print streamMapData
			i = 0
			while i < streamLen:
				if not cmp(desMap[0], streamMapData[i][0]) and not cmp(desMap[1], streamMapData[i][1]) \
					and not cmp(srcMap[0], streamMapData[i][10]) and not cmp(srcMap[1], streamMapData[i][11]):
					break
				i += 1
			if i == streamLen and 1 == flag:
# Position two and three denote rpack and ppack
				srcMap.append(1)
				srcMap.append(0)
				srcMap.append(streamInfo['len'])
				srcMap.append(streamInfo['len'])
				srcMap.append(0)
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
				streamMapData[i][10] = streamInfo['srcIP']
				streamMapData[i][11] = streamInfo['srcPort']
				streamMapData[i][3] += 1
				streamMapData[i][6] += streamInfo['len']
				tmp = []
				tmp.append(streamInfo['len'])
				streamMapData[i][9].extend(tmp)
				rpsizesum += streamInfo['len']
			k += 1
	finally:
#		print streamMapData
# Prepared for the Analysis
		i = 0
		j = 2
		fbpData = open(path+'tcpStatistic.txt', 'w')
		while i < streamLen:

#			print "%r" % (ipTrans(streamMapData[i][0])),
#			print "%r" % (portTrans(streamMapData[i][1])),
#			print "%r" % (ipTrans(streamMapData[i][10])),
#			print "%r" % (portTrans(streamMapData[i][11])),
#			print streamMapData[i][8]

			j = 2
			while j < 5:
				fbpData.write("%d " % streamMapData[i][j])
				j += 1
				
			rmsdLen = streamMapData[i][2]
			if 0 != rmsdLen:
				ravg = float(streamMapData[i][5])/streamMapData[i][2]
				ans = 0
				k = 0
				while k < rmsdLen:
					ans += pow(abs(streamMapData[i][8][k]-ravg),2)
					k += 1
				ans /= rmsdLen
				ans = pow(ans, 0.5)
				fbpData.write("%.2lf %.2lf " % (ravg, ans))
			else:
				fbpData.write("0.00 0.00 ")

			pmsdLen = streamMapData[i][3]
			if 0 != pmsdLen:
				pavg = float(streamMapData[i][6])/streamMapData[i][3]
				ans = 0
				k = 0
				while k < pmsdLen:
					ans += pow(abs(streamMapData[i][9][k]-pavg),2)
					k += 1
				ans /= pmsdLen
				ans = pow(ans, 0.5)
				fbpData.write("%.2lf %.2lf" % (pavg, ans))
			else:
				fbpData.write("0.00 0.00")
			fbpData.write("\n")
			i += 1
		fbpData.close()

		threshold = rpsizesum * attrMBThreshold
		i = 0
		while i < streamLen:
			if streamMapData[i][6] > threshold and streamMapData[i][7] > attrMBSYN:
				print "PacketStream %d Might be P2P" % (i+1)
			i += 1
		ftxt.close()
	
def tcpEngineRun(packetStreamBase, packetStreamData, packetInfo):
# packetStream is used to identify the network stream
# curStream: srcIP desIP srcPort desPort --> sorted()
# packetStreamBase: [[srcIP desIP srcPort desPort],[....]......]
# packetStreamData: [[payload],[...]....]

#	if len(packetInfo['payload']) != 0 and '\x13' == packetInfo['payload'][0]:
#		print "BitTorrent"
	curStream = []
	packetPort = []
	curStream.append(packetInfo['srcIP'])
	curStream.append(packetInfo['desIP'])
	curStream.sort()
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
	return packetStreamBase, packetStreamData




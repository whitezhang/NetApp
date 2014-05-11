from transEngine import ipTrans

def readUdpMatchingLib():
	lib = open('udplib.conf', 'rb')
	libName = []
	udpLib = []
	line = lib.readline()
	while line:
		line = line.replace('\r\n', '')
		libName.append(line)
		line = lib.readline()
		tmpLib = line.split(' ')[:]
		tmpLib[-1] = tmpLib[-1].replace('\r\n', '')
		for index in range(len(tmpLib)):
			tmpLib[index] = chr(int(tmpLib[index]))
		udpLib.append(tmpLib)
		line = lib.readline()
#	print libName,
#	print "%r"%udpLib
	lib.close()
	return libName, udpLib

def udpMatching(udpPacketStreamBase, udpPacketStreamData):
	libName, udpLib = readUdpMatchingLib()
	threshold = 10
	udpPacketStreamDataLen = len(udpPacketStreamData)
	udpLibLen = len(udpLib)
	print udpLibLen
	for i in range(udpPacketStreamDataLen):
		payload = udpPacketStreamData[i]
		payloadLen = len(payload)
		if payloadLen < 2:
			continue
#		print "====================%d"%payloadLen
#		print "%r"%payload
		j = 0
		while j < udpLibLen:
			tmpLib = udpLib[j]
			tmpLibLen = len(tmpLib)
			k = 0
			totalNum = 0
			while k < payloadLen:
				hashMap = {}
#				for m in range(tmpLibLen):
#					hashMap[tmpLib[m]] = 1
				singleLen = len(payload[k])
				singleLen = threshold if threshold < singleLen else singleLen
				for n in range(singleLen):
					hashMap[payload[k][n]] = 1
				flag = 0
				for n in range(tmpLibLen):
					if not hashMap.has_key(tmpLib[n]):
						flag = 1
						break
				if 0 == flag:
					totalNum += 1
					libIndex = j
				k += 1
#			print "total: %d"%totalNum
			if totalNum == payloadLen:
				print i,
				print payloadLen,
				print "%r" % ipTrans(udpPacketStreamBase[i][udpPacketStreamBase[i][2]]),
				print "%r: %r" % (libName[libIndex], tmpLib)
				break
			j += 1

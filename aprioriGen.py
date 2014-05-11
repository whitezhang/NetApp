def unique(listPar):
	length = len(listPar)
	revL = []
	i = 0
	while i < length:
		if listPar[i] not in revL:
			revL.append(listPar[i])
		i += 1
	return revL

def createD(udpPacketStreamData, lenFlag = 0, singleLength = 8):
	D = []
	k = 0
	lineLen = len(udpPacketStreamData)
	while k < lineLen:
		payload = udpPacketStreamData[k]
		payloadLen = len(payload)
		payloadStream = []
		i = 0
		while i < payloadLen:
			payloadList = []
			singleLen = len(payload[i])
			if 1 == lenFlag and singleLen > singleLength:
				singleLen = singleLength
			j = 0
			while j < singleLen:
				payloadList.append(payload[i][j])
				j += 1
			i += 1
			payloadStream.append(payloadList)
		D.append(payloadStream)
		k += 1
	return D

def udpAprioriGen():
	dataSet = []
	baseC = 0
	for i in range(256):
		dataSet.append(chr(baseC))
		baseC += 1
	return dataSet

def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return map(frozenset, C1)

def scanD(D, Ck, minSupport):
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not ssCnt.has_key(can): ssCnt[can]=1
				else: ssCnt[can] += 1
	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >= minSupport:
			retList.insert(0,key)
		supportData[key] = support
	return retList, supportData

def aprioriGen(Lk, k): #creates Ck
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1, lenLk): 
			L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
			L1.sort(); L2.sort()
			if L1==L2: #if first k-2 elements are equal
				retList.append(Lk[i] | Lk[j]) #set union
	return retList

def apriori(C1, D, minSupport = 0.5):
	D = map(set, D)
	L1, supportData = scanD(D, C1, minSupport)
	L = [L1]
	k = 2
	while (len(L[k-2]) > 0):
		Ck = aprioriGen(L[k-2], k)
		Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L, supportData

def aprioriFactory(dataSet, udpPacketStreamData, minSupport = 0.95, singleLength = 8):
	C1 = createC1(dataSet)
	D = createD(udpPacketStreamData, 1, singleLength)
	dLen = len(D)
	revL = []
	k = 0
	while k < dLen:
#	number of packet stream
#		print len(D[k])
		if len(D[k]) <= 5:
			k += 1
			continue
		L, suppData = apriori(C1, D[k], minSupport)
#	L feature
		print k,
		print len(D[k])
		print L[len(L)-2]
		revL.append(L[len(L)-2])
		k += 1
	return revL

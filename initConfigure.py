def readConfigure():
	fconf = open('info.conf', 'r')
	line = fconf.readline()
	while line:
		attributes = line.split(' ')
		if 'MarketBasketThreshold' == attributes[0]:
			attrMBThreshold = float(attributes[1])
		elif 'MarketBasketSYN' == attributes[0]:
			attrMBSYN = int(attributes[1])
		line = fconf.readline()
	fconf.close()
	return attrMBThreshold, attrMBSYN
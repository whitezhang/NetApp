def ipTrans(ipHex):
	ipAddress = []
	for i in range(4):
		ipAddress.append(ord(ipHex[i]))
	return ipAddress

def portTrans(portHex):
	port = ord(portHex[0])*16*16+ord(portHex[1])
	return port
from transEngine import *
import string

path = 'Data/TD/'

def writeUdpPacketStreamData(udpPacketStreamData):
	fName = path+'udpStream.txt'
	ftxt = open(fName, 'wb')
	try:
		for stream in udpPacketStreamData:
			for item in stream:
				ftxt.write("".join(item))
				ftxt.write("|$|")
			ftxt.write("|#|")
	except IOError, e:
		print "writeUdpPacketStreamData Error"
	else:
		pass
	finally:
		ftxt.close()

def writeFile(packetInfo, fileName):
	fName = path+fileName+'.txt'
	ftxt = open(fName, 'ab')
	try:
		ftxt.write(packetInfo['srcIP']
			+packetInfo['desIP']
			+packetInfo['srcPort']
			+packetInfo['desPort']
			+packetInfo['payload']
			)
		ftxt.write("|#|")
	except IOError, e:
		print "Write file error"
	else:
		pass
	finally:
		ftxt.close()

# Calculate the number
def writeStatisticFile(streamMapData, streamLen, fileName):
	i = 0
	fbpData = open(path+fileName+'.txt', 'w')
	while i < streamLen:
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
				ans += pow(abs(streamMapData[i][7][k]-ravg),2)
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
				ans += pow(abs(streamMapData[i][8][k]-pavg),2)
				k += 1
			ans /= pmsdLen
			ans = pow(ans, 0.5)
			fbpData.write("%.2lf %.2lf" % (pavg, ans))
		else:
			fbpData.write("0.00 0.00")
		fbpData.write("\n")
		i += 1
	fbpData.close()

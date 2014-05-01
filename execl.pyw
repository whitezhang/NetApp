import xlwt

def readUDPFile():
	path = 'Data/TD/'
	fName = path+'udpNeuro.txt'
	ftxt = open(fName, 'rb')
	try:
		allLines = ftxt.readlines()
	except IOError, e:
		print "No file name"
	else:
		pass
	finally:
		ftxt.close()
		return allLines

def execl():
	wbk = xlwt.Workbook()
	sh = wbk.add_sheet('sheet 1')

	i = 1
	allLines = readUDPFile()
	for eachLine in allLines:
		lineNum = eachLine.split(' ')
		lineLen = len(lineNum)
		sh.write(i, 1, lineNum[0])
		sh.write(i, 4, lineNum[1])
		sh.write(i, 2, lineNum[3])
		sh.write(i, 3, lineNum[4])
		sh.write(i, 5, lineNum[5])
		sh.write(i, 6, lineNum[6])
		i += 1

	wbk.save('udp.xls')

execl()
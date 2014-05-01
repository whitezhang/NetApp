Author: Wyatt Zhang
Start from 06/03/2014
======================= File formation ======================

tcp.txt('|#|')
	srcIP desIP srcPort desPort length flag payload

udp.txt('|#|')
	srcIP desIP srcPort desPort payload

udpPending.txt('|#|')
	srcIP desIP srcPort desPort payload

udpStream.txt('|#|'\'|$|') --> pending
	payload

tcpStatistic.txt
	rbyte pbyte rhbyte1 ravg rmsd pavg pmsd

udpStatistic.txt
	rbyte pbyte rhbyte1 ravg rmsd pavg pmsd

udpPendingStatistic.txt
	rbyte pbyte rhbyte1 ravg rmsd pavg pmsd

apriori.txt --> udp

======================= Problems ============================

4G memory is not able to store the whole data, test error
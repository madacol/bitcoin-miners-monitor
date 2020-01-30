import re, requests, time, os, sys

print time.asctime(time.localtime(time.time()))

pid = str(os.getpid())
pidfile = "/tmp/SendData.pid"

if os.path.isfile(pidfile):
	print "%s already exists, exiting" % pidfile
	os.system( "printf '"+pidfile+" already exists' | mail -s 'ERROR in SendData - another instance already exist' root")
	sys.exit()
else:
    file(pidfile, 'w').write(pid)

urlStrings = {
	'161' : { 'key':'1mse8q4zwGEBweUnkD91s8xpNrTxJTR2zgavDsdSggAI','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'777544372='},
	'162' : { 'key':'1o9J-dmGg-TidKoBtu8I1bfYFaHy9HjC-69WDieNMK5o','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'407889139='},
	'163' : { 'key':'1q8Zj_6ahmb4bmOVSJYswr7Jun2mbdGaYly8W5tDODhM','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1702644564='},
	'164' : { 'key':'1OZHB0tQ1zm0S1Dl9BET1cLt6D5VNE9MnG10XJAIMQt4','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1085538469='},
	'165' : { 'key':'1E2mik4xehGmhRKgFQzCOw--p9hkwaTB9dZTvPx6T6oY','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1275624298='},
	'166' : { 'key':'1ebEort_bUtkZBiZXZh-JRLSeQReROm1VBsavGkCPFS8','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1309109464='},
	'167' : { 'key':'17VUsPNU6x3F4jLvB0gGmV_dJBUAKKlRV4Tnpv5_aDZ4','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1071261380='},
	'168' : { 'key':'1DyI_XQ-xs5KFYLBosllS-_p1_3p9W9JDy1LnCB8_Vq8','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'847033218='},
	'169' : { 'key':'1UBRPLlZb4pIPtHrb08ahnGocaWfivm2Fgff7badDvV0','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1583679740='},
	'170' : { 'key':'1yld8Hj8oHqXyJuWZu7dmn2LsOIODuBfyypoSsohVssU','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'77414610='},
	'171' : { 'key':'1zPiZ_aEdA6dcqFMGNCLgjLTOtYzlRraFdGfkrNSeVrw','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'741974560='},
	'172' : { 'key':'1DdBRFB1B1lWPNlT41YxEWokLyA3oAbiKM6okJ4HwGpI','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'94791089='},
	'173' : { 'key':'1PZ2nU0GWgf0F8KLplQxELuisP1J7kdQFazhkNfhmJTY','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1250319218='},
	'174' : { 'key':'1RHqmt4N8SkYpHPD-xneH542gqHHnEuJPk659UOKcINw','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1546687668='},
	'175' : { 'key':'1mYiXq5rUDN9ayIucdO-PJ7PGC38920MsL62of_hOwNw','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'994153201='},
	'176' : { 'key':'1qVX4XKeQFMIIosybuAW7s76vPBKzpj3099-Ozj0_pQs','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1657052425='},
	'177' : { 'key':'1z96Zg89glYhmlD9rj2K9cNsdksaWTcbJoZPg5kx3xlI','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'958164499='},
	'178' : { 'key':'1uRLox4rjJy6l-Pm5_--CE_zOSjO2Gc9KGfGjgBhLHP4','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1747857998='},
	'179' : { 'key':'1ID9lXUFbcNFUQ0z5j3WRI0YxsEx29e92bQWx3_wo7Gw','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'964952321='},
	'180' : { 'key':'1y-ZQMRl5R_wYmzYIrZLCygaI6GAParbXV3ZBimQTtDs','ip':'1109145402=','temp0':'1194320442=','temp1':'822120583=','ghs':'1295295883=','pool':'1928010676=','asics':'423374287=','error':'1577444996=','timestamp':'1136290660='},
}

with open('miners/dataTOsend.csv','r') as sendfile:
	for line in sendfile:
		data = line.split(',')
		if len(data) >= 7:
			timestamp = data[0]
			ip = data[1]
			ghs = data[2]
			temp0 = data[3]
			temp1 = data[4]
			pool = data[5]
			asics = data[6]
			try:
				requests.head('https://docs.google.com/forms/d/'+urlStrings[ip]['key']+'/formResponse?ifq&entry.1109145402='+ip+'&entry.1194320442='+temp0+'&entry.822120583='+temp1+'&entry.1295295883='+ghs+'&entry.1928010676='+pool+'&entry.423374287='+str(asics)+'&entry.'+urlStrings[ip]['timestamp']+timestamp+'&submit=Submit', timeout=50)
			except Exception as e:
				print 'Not sent'
				error = 'Failed to send data. data='+str(data)+' | e='+str(e)
				with open('miners/errors.txt','a') as errorfile:
					print >> errorfile, error
				with open('miners/dataTOsend.csv.tmp','a') as tmpsendfile:
					print >> tmpsendfile, line[0:-1]
		else:
			with open('miners/errors.txt','a') as errorfile:
				currentPosition = sendfile.tell()
				sendfile.seek(0)
				dataTOsend = sendfile.read()
				sendfile.seek(currentPosition)
				print >> errorfile, 'ERROR - data < 7\ndataTOsend.csv='+str(dataTOsend)
				os.system('printf "ip='+str(ip)+'\n\ndataTOsend.csv:\n'+str(dataTOsend)+'" | mail -s "ERROR in SendData - data < 7" root')

if os.path.exists('miners/dataTOsend.csv.tmp'):
	os.rename ('miners/dataTOsend.csv.tmp','miners/dataTOsend.csv')
else:
	os.remove('miners/dataTOsend.csv')

os.remove(pidfile)

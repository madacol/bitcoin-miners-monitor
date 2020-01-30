import re, requests, time

print time.asctime(time.localtime(time.time()))

for ip in range(161,181):		#Iterate through a range of ip (161,181 actually means 161-180)
#Preparing request to cgminer's API
	req = requests.Request(' ', 'http://192.168.10.'+str(ip)+':4028')
	r = req.prepare()
	r.method = 'stats+pools|'
	s = requests.Session()
	try:
		s.send(r)	#Send request to miner
	except requests.exceptions.ConnectionError as e:
		data = str(e)	#Data received
		try:	#Extracting information from data
			ghs = re.search('(?<=GHS 5s=)[^,]+?(?=,)',data).group(0)
			pool = re.search('(?<=URL=)[^,]+?(?=,Status=Alive)',data).group(0)
			asics = re.findall('(?<=chain_acs\d=)(?!,)[^,]+?(?=,)',data)
			temp = re.findall('(?<=temp\d=)(?!0)[^,]+?(?=,)',data)
			try:	#Send info to Google Form, sometimes fails because it times out or an EOF ssl error (Don't know how to fix this one)
				requests.head('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1194320442='+temp[0]+'&entry.822120583='+temp[1]+'&entry.1295295883='+ghs+'&entry.1928010676='+pool+'&entry.423374287='+str(asics)+'&submit=Submit', timeout=50)
			except Exception as e2:
				error = 'Failed to send data (1st try). data='+data[0:500]+' | e='+str(e)+' | e2='+str(e2)
				print '\n',error,'\n'
				#Trying again to send the info with error included, sometimes this info gets duplicated when the former succeeds sending the info but the response get timed out
				try:
					requests.head('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1194320442='+temp[0]+'&entry.822120583='+temp[1]+'&entry.1295295883='+ghs+'&entry.1928010676='+pool+'&entry.423374287='+str(asics)+'&entry.1577444996='+error+'&submit=Submit', timeout=50)	#Send info to Google Form			
				except Exception as e3:
					print 'Failed to send data (2nd try). | e3=',str(e3),' | error=',error		
		except Exception as e:
			error = 'RegExp FAILED, Raw data Invalid. | data='+data[0:500]+' | e='+str(e)
			print '\n',error,'\n'
			requests.head('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1577444996='+error+'&submit=Submit')
	except Exception as e:
		error = 'Miner request FAILED. data='+data+'   e='+str(e)
		print '\n',error,'\n'
		requests.head('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1577444996='+error+'&submit=Submit')
	data=e=e2=ghs=pool=asics=temp=error=''	#Flush variables	
	print str(ip),' Loop finished\n'

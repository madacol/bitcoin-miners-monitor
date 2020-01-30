import re, requests, os
from datetime import datetime

for ip in range(161,181):		#Iterate through a range of ip (161,181 actually means 161-180)
#Preparing request to cgminer's API
	data=e=e2=ghs=pool=asics=temp0=temp1=error=newline=status=''	#Flush variables	
	req = requests.Request(' ', 'http://192.168.10.'+str(ip)+':4028')
	r = req.prepare()
	r.method = 'stats+pools|'
	s = requests.Session()
	#Constructing a timestamp
	year = str(datetime.now().year)
	month = str(datetime.now().month)
	day = str(datetime.now().day)
	hour = str(datetime.now().hour)
	minute = str(datetime.now().minute)	
	timestamp = year+'-'+month+'-'+day+'+'+hour+':'+minute	
	try:
		s.send(r)	#Send request to miner
	except requests.exceptions.ConnectionError as e:
		data = str(e)	#Data received	
		if re.search('error',data): # Check
			error = data[0:100]
			status = 'OFF'
		else:
			try:	#Extracting information from data
				status = 'ON'
				ghs = re.search('(?<=GHS 5s=)[^,]*?(?=,)',data)
				if ghs:
					ghs = str(ghs.group(0))
				else:
					ghs = ''
					error += 'ghs - No match - (?<=GHS 5s=)[^,]*?(?=,)'
				pool = re.search('(?<=URL=)[^,]*?(?=,Status=Alive)',data)
				if pool:
					pool = str(pool.group(0))
				else:
					pool = 'Dead???'
					error +=  'pool - No match - (?<=URL=)[^,]*?(?=,Status=Alive)'
				asics = re.findall('(?<=chain_acs\d=)[^,]*?(?=,)',data)
				if asics[0] and asics[1]:
					asics = asics[0] + '| ' + asics[1]
				else:
					asics = asics[0] + asics[1]
					error += 'asics - chain_asics missing??'
				temp = re.findall('(?<=temp\d=)[^,]*?(?=,)',data)
				if temp:
					temp0 = temp[0]
					temp1 = temp[1]
				else:
					temp1=temp0=0				
			except Exception as e:
				error += 'RegExp FAILED, Raw data Invalid. | data='+data[0:500]+' | e='+str(e)
				print '\n',error,'\n'
			else:
				# Restart miner if pools are dead or if there's High temperature
				if pool == 'Dead???' or max(int(temp1),int(temp0)) >= 60:
					os.system('python /home/pi/miners/RestartMiners.py 192.168.10.' + str(ip) )
					if pool == 'Dead???':
						mailSubject = 'Pool Dead on '+str(ip)+' - Restarting'
					else:
						mailSubject = 'High Temp on '+str(ip)+' - Restarting'
					mailMessage = 'pool='+pool+'\ntemps='+str(temp0)+'-'+str(temp1)
					os.system('printf "'+mailMessage+'" | mail -s "'+mailSubject+'" root')	
		
		newline = timestamp+','+ghs+','+temp0+','+temp1+','+pool+','+asics+','+error
		try:
			with open('miners/'+str(ip)+'data.csv','a') as f:
				print >> f, newline			
			with open('miners/'+str(ip)+'dataTMP.csv','a') as f:
				print >> f, newline
			if os.path.exists('miners/'+str(ip)+'status.txt'):
				with open('miners/'+str(ip)+'status.txt','r+') as f:					 
					oldStatus = f.read()
					mailMessage = 'newline='+newline
					if oldStatus == 'ON' and status == 'OFF':
						os.system('python /home/pi/miners/RestartMiners.py 192.168.10.' + str(ip) )
						mailSubject = str(ip)+'miner OFF - trying ssh restart'
						os.system('printf "'+mailMessage+'" | mail -s "'+mailSubject+'" root')	
					elif oldStatus == 'OFF' and status == 'ON':
						mailSubject = str(ip)+'miner is back ON'	
						os.system('printf "'+mailMessage+'" | mail -s "'+mailSubject+'" root')	
					f.seek(0)							
					f.truncate()
					f.write(status)
			else:
				with open('miners/'+str(ip)+'status.txt','w') as f:
					f.write(status)
		except Exception as e:
			error += 'Failed to write data to a file. newline='+newline+' | e='+str(e)+' | status='+status
			print '\n',error,'\n'
	except Exception as e:
		error = 'Miner request FAILED. data='+data+'   e='+str(e)
	if error:
		with open('miners/errors.txt','a') as f:
			print >> f, str(ip) + ', ' + timestamp +', error=' + error
	print newline ,'\n'+str(ip)+' Loop finished\n'
import os
from datetime import datetime
from decimal import Decimal

with open('miners/dataTOsend.csv','a') as sendfile:
	for ip in range(161,181):
		lastpool=pool=asics=''
		i=ghs=temp0=temp1=0
		file = 'miners/'+str(ip)+'dataTMP.csv'
		if os.path.exists(file):
			with open(file,'r') as tmpfile:
				for line in tmpfile:
					data = line.split(',')
					if len(data) >= 7:
						if data[1]:
							ghs += Decimal(data[1])
						else:
							ghs = 0
						if data[2]:
							temp0 += Decimal(data[2])
						else:
							temp0 = 0
						if data[3]:
							temp1 += Decimal(data[3])
						else:
							temp1 = 0
						if lastpool and lastpool != data[4]:
							pool += data[4]
						lastpool = data[4]
						if not asics or asics.count('x')+asics.count('-') > data[5].count('x')+data[5].count('-'):
							asics = data[5]
						i+=1
					else:						
						with open('miners/errors.txt','a') as errorfile:
							print >> errorfile, 'ERROR - data < 8\nip='+str(ip)+' - data='+str(data)
			if i:
				ghs = str(ghs / i)
				temp0 = str(temp0 / i)
				temp1 = str(temp1 / i)
			pool = lastpool + pool
			year = datetime.now().year
			month = datetime.now().month
			day = datetime.now().day
			hour = datetime.now().hour
			minute = datetime.now().minute
			timestamp = '%04d'%year+'-'+'%02d'%month+'-'+'%02d'%day+'+'+'%02d'%hour+':'+'%02d'%minute
			newline = timestamp+','+str(ip)+','+ghs+','+temp0+','+temp1+','+pool+','+asics+','
			print >> sendfile, newline
			os.remove(file)

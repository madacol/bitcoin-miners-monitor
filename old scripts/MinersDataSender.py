import re, requests

for ip in range(161,181):		#Iterate through a range of ip (161,181 actually means 161-180)
	req = requests.Request(' ', 'http://192.168.10.'+str(ip)+':4028')
	r = req.prepare()
	r.method = 'stats+pools|'
	s = requests.Session()
	try:
		s.send(r)
	except requests.exceptions.ConnectionError as e:
		data = str(e)
		try:
			ghs = re.search('(?<=GHS 5s=)[^,]+?(?=,)',data).group(0)
			pool = re.search('(?<=URL=)[^,]+?(?=,Status=Alive)',data).group(0)
			asics = re.findall('(?<=chain_acs\d=)(?!,)[^,]+?(?=,)',data)
			temp = re.findall('(?<=temp\d=)(?!0)[^,]+?(?=,)',data)
			requests.get('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1194320442='+temp[0]+'&entry.822120583='+temp[1]+'&entry.1295295883='+ghs+'&entry.1928010676='+pool+'&entry.423374287='+str(asics)+'&submit=Submit')
		except Exception as e:
			error = 'RegExp or Send FAILED. data='+data[0:100]+'   e='+str(e)
			print '\n',error,'\n'
			requests.get('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1577444996='+error+'&submit=Submit')
	except Exception as e:
		error = 'Miner request FAILED. data='+data+'   e='+str(e)
		print '\n',error,'\n'
		requests.get('https://docs.google.com/forms/d/1vzV9boocCp0OyqtCwmOuLWyiBXzXPs5UdsAnNY7cK98/formResponse?ifq&entry.1109145402='+str(ip)+'&entry.1577444996='+error+'&submit=Submit')

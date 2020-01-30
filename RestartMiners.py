import pxssh, sys
for ip in sys.argv[1:]:
	try:
		s = pxssh.pxssh()
		hostname = str(ip)
		username = 'root'
		password = 'admin'
		s.login(hostname, username, password)
		s.sendline('reboot')   # run a command
		s.prompt()  
		print('OK')
	except pxssh.ExceptionPxssh as e:
		print("pxssh failed on login.")
		print(e)
	except Exception as e:
		print('script failed')
		print(e)
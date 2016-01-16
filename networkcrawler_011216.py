#! /usr/bin/python

# This work is licensed under the GNU General Public License v3.0
#
# This script crawls a Cisco network but can be easily modified for any network devices
# running LLDP. This script is the basic engine to crawl a network. Extension ideas could be 
# to add DNS lookups on the IP addresses, create a network diagrams, etc...
#
# The Network Crawler script outputs an file connections.txt that contains a full CDP connection
# table in CSV format. You can extract a node table by modifying the code to output a seperate 
# target file or you can grab the notes by simply taking the information from the CSV file.
#
# Dependencies pexpect (Python Expect). You will need to load this module before the
# Network Crawler will work.
# Dependencies - Also make sure your python path is correct it's usually usr/bin/python
#
# This version clears the just_crawled variable after each cdp crawl.

import pexpect

# Please place your seed device in the to_crawl list.
# modify the to_crawl list. i.e. to_crawl = ['yourrouter1']

seed = raw_input('Enter One Seed Device: ')
user = raw_input('Username? ')
passwd = raw_input('Password? ')

to_crawl = [seed]
crawl_ed = []
just_crawled = []

def cdpcommand(switch_ip,switch_un,switch_pw):
	
	cdpout = [switch_ip]
	child = pexpect.spawn('telnet %s' % (switch_ip))
	child.logfile = open("./mylog", "w")
	loginresult = child.expect(['[Uu]sername','[Pp]assword'])
	child.timeout = 2
	if loginresult == 1:
		child.sendline(switch_pw)
		child.expect('[Ll]ogin')
		child.sendline(switch_un)
		child.expect('[Pp]assword:')
		child.sendline(switch_pw)
               	child.expect('#')
               	child.sendline('terminal length 0')
               	child.expect('#')
               	child.sendline('show cdp entry *')
                child.expect('#')
               	child.sendline('show cdp entry all')
               	child.expect('#')
               	child.logfile.close()
	elif loginresult == 0:
		child.sendline(switch_un)
		child.expect('[Pp]assword:')
		child.sendline(switch_pw)
		child.expect('#')
		child.sendline('terminal length 0')
		child.expect('#')
		child.sendline('show cdp entry *')
                child.expect('#')
		child.sendline('show cdp entry all')
		child.expect('#')
		child.logfile.close()
	else:
			exit

	routerFile = open('./mylog', 'r')
	datalist = routerFile.read()
	routerFile.close()
	
	indexer = 0
	count = 0

# You would modify this section if you were trying to make this work for another
# vendor using LLDP

	while indexer != -1:
                indexer = datalist.find("Device ID:",count)
                if indexer == -1:
                        exit
                endindexer = datalist.find("\r",indexer)
                count = endindexer + 1
		word = datalist[indexer:endindexer]
		if indexer != -1:
                	if "(" in word:
				paranthesis = word.find("(")
				cdpout.append(datalist[indexer + 10:indexer + paranthesis])
			else:
				cdpout.append(datalist[indexer + 10:endindexer])
        return cdpout



connections = open('./connections.txt', 'w')
while to_crawl:
	target = to_crawl.pop()
	just_crawled = []
	try:
		just_crawled = cdpcommand(target,user,passwd)
	except OSError:
		crawl_ed.append(target)
	except pexpect.EOF:
		crawl_ed.append(target)
	except pexpect.TIMEOUT:
		crawl_ed.append(target)
	else:
		crawl_ed.append(target)
	for item in just_crawled:
		if 'VW0' in item:
			crawl_ed.append(item)
                if 'NAC' in item:
                        crawl_ed.append(item)
                if 'NAS' in item:
                        crawl_ed.append(item)
                if 'nac' in item:
                        crawl_ed.append(item)
                if 'nas' in item:
                        crawl_ed.append(item)
                if 'ccp' in item:
                        crawl_ed.append(item)
                if 'CCP' in item:
                        crawl_ed.append(item)
                if 'VOIP' in item:
                        crawl_ed.append(item)
                if 'voip' in item:
                        crawl_ed.append(item)
		if 'sep' in item:
			crawl_ed.append(item)
		if 'SEP' in item:
			crawl_ed.append(item)
		if 'AP' in item:
			crawl_ed.append(item)
		if 'ap' in item:
			crawl_ed.append(item)
		if item not in crawl_ed:
			if item not in to_crawl:
				to_crawl.append(item)
	
	print "to_crawl variable"
#	print ""
	print to_crawl
	print ""
	print "just_crawled variable"
#	print ""
	print just_crawled
	print ""
	print "crawlED variable"
#	print ""
	print crawl_ed
	for listitem in just_crawled:
		connections.write(target)
		connections.write(",")
		connections.write(listitem)
		connections.write("\n")

connections.close()

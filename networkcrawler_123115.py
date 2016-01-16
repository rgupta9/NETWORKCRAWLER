#! /usr/bin/python

# This work is licensed under the GNU General Public License v3.0
#
# This script crawls a Cisco network but can be easily modified for any network devices
# running LLDP. This script is the basic engine to crawl a network. Extension ideas could be 
# to add DNS lookups on the IP addresses, create a network diagrams, etc...
#
# Dependencies pexpect (Python Expect). You will need to load this module before the
# Network Crawler will work.

import pexpect

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
	child.timeout = 10
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


while to_crawl:
	target = to_crawl.pop()
	try:
		# remember to put your username and password in the line below
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
		if item not in crawl_ed:
			if item not in to_crawl:
				to_crawl.append(item)
	
	print "to_crawl variable"
	print ""
	print to_crawl
	print ""
	print "just_crawled variable"
	print ""
	print just_crawled
	print ""
	print "crawlED variable"
	print ""
	print crawl_ed

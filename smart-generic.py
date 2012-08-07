#! /usr/bin/env python
# Copyright (C) 2012 Nigel Roberts
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Put SMART parameter ID on command line, prefixed by 'R' if you want raw value
#
# Put "worst" on the command line and the smallest gap to threshold of all
# parameters will be output.

import getopt, glob, re, sys, os

path = '/var/lib/smartmontools'

showdev, showid, showraw = 0, -1, 0

try: 
	opts, args = getopt.getopt(sys.argv[1:],'dri:')
except getopt.GetoptError:
	print 'snmp-smart.ph -d'
	print 'snmp-smart.py [-r] -i <id>'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-d':
		showdev = 1
	if opt == '-i':
		showid = arg
	if opt == '-r':
		showraw = 1

os.chdir(path)
statefiles = glob.glob('smartd.*.state')

devices = {}
i = 0

for filename in statefiles:
	m1 = re.search('(?<=-)([\w]+)', filename)
	serial = m1.group(0)
	devices[serial] = {'filename': filename}

if showdev != 0:
        for k, v in devices.iteritems():
                print k
        exit

valid = re.compile("([\w-]+)\.(\d+)\.(\w+) = (\d+)")

for serial, v in devices.iteritems():
	with open(devices[serial]['filename']) as f:
		attr = {}
		id = 0
		for line in f:
			m2 = valid.search(line)
			if m2 is not None:
				if m2.group(3) == 'id':
					id = m2.group(4)
					devices[serial][id] = {}
				else:
					devices[serial][id][m2.group(3)] = m2.group(4)

if showid != -1:
	for k, v in devices.iteritems():
		if showraw == 1:
			if showid == '194' or showid == '190':
				# special case for temperature values
				# actual temperature is in the last 2 bytes
				raw = int(devices[k][showid]['raw']) & 0xff 
			else:
				raw = devices[k][showid]['raw']
			print raw
		else:
			print devices[k][showid]['val']

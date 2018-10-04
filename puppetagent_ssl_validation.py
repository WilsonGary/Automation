#!/usr/bin/python

import os
import xlrd



xls = '/apps/zeomega/src/puppet/puppetmaster_software/deployer/abctest_61_prod.xlsx'
jivabook = xlrd.open_workbook(xls)
jivasheet = jivabook.sheet_by_name('Server List')
serverlist_column = jivasheet.col_values(1, 2)
server_list = map(lambda x: x.lower(), serverlist_column)

puppet_cert_cmd = 'puppet cert list --all'
puppet_singed = os.popen(puppet_cert_cmd).read()

for fqdn in server_list:
	if fqdn not in puppet_singed:
		print fqdn, "is NOT SIGNED with PuppetMaster"
	else:	
		print fqdn, "is Successfully Signed with PuppetMaster"

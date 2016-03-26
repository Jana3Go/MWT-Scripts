import os
import re
import pprint
import json
import textwrap
from collections import defaultdict

# Change working directory to the scripts base directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

macportfile = 'macaddress-table.txt'
arpfile = 'arp-table.txt'

pmac = re.compile('[0-9a-h]{4}\.[0-9a-h]{4}\.[0-9a-h]{4}')
pport = re.compile('(Ten|Po|Fa|Gi|Eth)(.*)')
pip = re.compile('(?:[0-9]{1,3}\.){3}[0-9]{1,3}')

with open(macportfile, 'r') as f:
    macportlist = f.readlines()

with open(arpfile, 'r') as f:
    arplist = f.readlines()

lmacip = {}
lportmac = {}
lmapping = defaultdict()

for l in arplist:
    mmac = pmac.search(l)
    mip = pip.search(l)
    if mmac and mip:
        lmacip.update({mmac.group(): mip.group()})

pp = pprint.PrettyPrinter(indent=4)
for l in macportlist:
    mmac = pmac.search(l)
    mport = pport.search(l)
    if mmac and mport:
        lmapping.setdefault(mport.group(), {})
        lmapping[mport.group()].update({mmac.group():{}})
        if mmac.group() in lmacip:
            lmapping[mport.group()][mmac.group()] = lmacip[mmac.group()]
#pp.pprint(lmapping)
print(json.dumps(lmapping, sort_keys=True, indent=4))

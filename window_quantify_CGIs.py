"""
window_quantify_CGIs.py

usage: python window_quantify_CGIs.py <windowfile.txt> <CGI.gff> <out.txt>
"""

import sys
from decimal import * 

out = open(sys.argv[3], 'w')

out.write('chrom'+'\t'+'start'+'\t'+'end'+'\t'+'CGIs'+'\t'+'CGI_bases'+'\t'+'prop_CGI_bases'+'\n')

windows = []

for line in open(sys.argv[1], 'r'):
	windows.append(line)

cgis = []

for line in open(sys.argv[2], 'r'):
    li=line.strip()
    if not li.startswith("#"):
		chrom = li.split('\t')[0]
		start = li.split('\t')[3]
		end = li.split('\t')[4]
		length = abs(int(end) - int(start))
# 		print length
		cgis.append(chrom+'_'+start+'_'+end+'_'+str(length))
# for i in repeats:
# 	print i

for window in windows:
	total = 0
	size = int(window.split()[2]) - int(window.split()[1])
	
	matches = [c for c in cgis if c.split('_')[0] == window.split()[0] and int(c.split('_')[1]) > int(window.split()[1]) and int(c.split('_')[2]) < int(window.split()[2])]
	for m in matches:
		length = m.split('_')[3]
		
		total = total + int(length)
	
	getcontext().prec = 11
	prop = Decimal(total)/Decimal(size)
	num = len(matches)
	out.write(window.split()[0]+'\t'+window.split()[1]+'\t'+window.split()[2]+'\t'+str(num)+'\t'+str(total)+'\t'+str(prop)+'\n')

"""
window_ldhat_r.py

This script will scan a results file generated using results from the LDhat interval and stat programs.
Using a genomic windows file with chrom, start, and end columns,
will calculate the average population scaled recombination rate per window.

IMPORTANT: this script assumes that the user is specifying a window file for the correct chromosome!

Notes: 

The loci in the res.txt file from LDhat are in kb format (e.g., 3.500 = 3500).
These need to be transformed into base pairs by removing the '.' in each entry.

The res.txt file contains a header line and a second line that summarizes the entire map length for the population.
This should be ignored.

Fields in the res.txt file are Loci, Mean_rho, Median, L95, and U95.

usage: python window_ldhat_r.py <windowfile.txt> <ldhat_res_file> <out.txt>
"""


import sys
from decimal import * 

out = open(sys.argv[3], 'w')
out.write('chrom'+'\t'+'start'+'\t'+'end'+'\t'+'snps'+'\t'+'mean_rho'+'\t'+'median'+'\t'+'l95'+'\t'+'u95'+'\n')

windows = []

#Read in window file and append windows
for line in open(sys.argv[1], 'r'):
	windows.append(line)

rates = []

#Read in LDhat results file and skip header and population lines:
with open(sys.argv[2], 'r') as f:
    results = f.readlines()[2:]
    for r in results:
    	loc = r.split()[0]
    	loc = loc.replace('.', '')
    	rho = r.split()[1]
    	med = r.split()[2]
    	l95 = r.split()[3]
    	u95 = r.split()[4]
    	rates.append(loc+'_'+rho+'_'+med+'_'+l95+'_'+u95)
    	
for window in windows:

#starting values for stat totals
	rho = 0
	med = 0
	l95 = 0
	u95 = 0

#look for locus matches in windows
	matches = [r for r in rates if int(r.split('_')[0]) > int(window.split()[1]) and int(r.split('_')[0]) < int(window.split()[2])]
#calculate the number of matches for calculating averages per window
	total = len(matches)
	if int(total) == 0:
		out.write(window.split()[0]+'\t'+window.split()[1]+'\t'+window.split()[2]+'\t'+str(total)+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\n')
	else:
#extract stats for each match and add to running totals for the window
		for m in matches:
			rh = m.split('_')[1]
			me = m.split('_')[2]
			l9 = m.split('_')[3]
			u9 = m.split('_')[4]
	
			rho = rho + float(rh)
			med = med + float(me)
			l95 = l95 + float(l9)
			u95 = u95 + float(u9)

#calculate stat means for genomic window
		getcontext().prec = 11
		
		avgrho = Decimal(rho)/Decimal(total)
		avgmed = Decimal(med)/Decimal(total)
		avgl95 = Decimal(l95)/Decimal(total)
		avgu95 = Decimal(u95)/Decimal(total)

#	print window.split()[0], window.split()[1], window.split()[2], avgrho, avgmed, avgl95, avgu95
	
		out.write(window.split()[0]+'\t'+window.split()[1]+'\t'+window.split()[2]+'\t'+str(total)+'\t'+str(avgrho)+'\t'+str(avgmed)+'\t'+str(avgl95)+'\t'+str(avgu95)+'\n')

	


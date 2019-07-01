"""
identify_hotspots.py

Author: Drew Schield [01/23/19]

This script is designed to identify genomic regions with exceptional recombination rate
relative to the regional background. The size of potential hotspot regions (i.e., windows)
is determined by the input, but the size of the background region is up to the user.

The background region is made up of upstream and downstream regions of a given length.
This length must be a multiple of the length of analyzed windows.

For example, if 3 kb windows are analyzed, you could choose a background of 18 kb, 21 kb, 24 kb.
These would correspond to total background regions of 36 kb, 42 kb, and 48 kb, respectively.

Here's the idea:

						Compare these to focal region
			  /\--------------------------------------------/\
  			 /	\										   /  \
 			/	 \					 3 kb				  /	   \
		Upstream Background		 Focal Region	   Downstream Background
5'|-------------------------------| |----| |-------------------------------|3'
								     \  /
									  \/
								Is this a hotspot?

Input for this script is a windowed recombination output file generated using the scripts:
1. window_LDhat_results_3kb_1kb.sh
2. concatenate_windows_3kb_1kb.sh

Note: the script names may be different, depending on the window sizes analyzed/binned.

Input format is tab-delimited and looks like:

chrom	start	end	snps	mean_rho	median	l95	u95

scaffold-ma1	10000	13000	1	0.83768000000	0.0019700000000	0.00025000000000	3.5041200000
scaffold-ma1	11000	14000	1	0.83768000000	0.0019700000000	0.00025000000000	3.5041200000
scaffold-ma1	12000	15000	1	0.83768000000	0.0019700000000	0.00025000000000	3.5041200000

Also, requires an input list of chromosomes to analyze. For example:

scaffold-ma1
scaffold-ma2
...

Input variables to consider:
1) size of background region
2) how extreme a hotspot has to be to be called (e.g., 5x background?)

usage:
python identify_hotspots.py <input.txt> <chromosome_list> <flanking_region_size> <hotspot_heat> <output.txt> <hotspot_summary.txt>

"""

import sys
import decimal
import numpy as np

flank = int(sys.argv[3])
heat = int(sys.argv[4])

full_out = open(sys.argv[5], 'w')
hspt_summ = open(sys.argv[6], 'w')

full_out.write('chrom'+'\t'+'start'+'\t'+'end'+'\t'+'window_snps'+'\t'+'background_snps'+'\t'+'background_windows'+'\t'+'window_rho'+'\t'+'background_rho'+'\t'+'heat'+'\n')
hspt_summ.write('chrom'+'\t'+'start'+'\t'+'end'+'\t'+'window_snps'+'\t'+'background_snps'+'\t'+'background_windows'+'\t'+'window_rho'+'\t'+'background_rho'+'\t'+'heat'+'\n')

chroms = []

for line in open(sys.argv[2], 'r'):
	chrom = line.split()[0]
	chroms.append(chrom)
	
for c in chroms:
	windows = []
	background = []
	with open(sys.argv[1], 'r') as input:
		next(input)
		for line in input:
			if line.split()[0] == c:
				windows.append(line.split('\n')[0])
				background.append(line.split('\n')[0])

	for w in windows:
		chrom = w.split()[0]
		start = w.split()[1]
		end = w.split()[2]
		wsnps = w.split()[3]
		wrho = w.split()[4]
		
		bgsnps = 0
		bgwindows = 0
		bg = []

		
		if wrho != 'NA':
			for b in background:
				if int(b.split()[1]) >= (int(start) - flank) and int(b.split()[2]) <= int(start) or int(b.split()[2]) <= (int(end) + flank) and int(b.split()[1]) >= int(end):

					bsnps = b.split()[3]
					bgsnps = bgsnps + int(bsnps)
					
					brho = b.split()[4]
					if brho != 'NA':
						bg.append(brho)
						bgwindows = bgwindows + 1
			
			bgnum = np.array(bg).astype(np.float)
			bgmean = np.mean(bgnum)
			
			rhoratio = float(wrho) / bgmean
			
			if rhoratio > float(heat):
				hspt_summ.write(chrom+'\t'+start+'\t'+end+'\t'+str(wsnps)+'\t'+str(bgsnps)+'\t'+str(bgwindows)+'\t'+str(wrho)+'\t'+str(bgmean)+'\t'+str(rhoratio)+'\n')

			full_out.write(chrom+'\t'+start+'\t'+end+'\t'+str(wsnps)+'\t'+str(bgsnps)+'\t'+str(bgwindows)+'\t'+str(wrho)+'\t'+str(bgmean)+'\t'+str(rhoratio)+'\n')
		else:
			full_out.write(chrom+'\t'+start+'\t'+end+'\t'+str(wsnps)+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\t'+'NA'+'\n')

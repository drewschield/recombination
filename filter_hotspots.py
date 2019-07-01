"""
filter_hotspots.py

Takes in a file generated using the identify_hotspots.py script, a distance window, and outputs the high-point hotspot window.

usage:

python filter_hotspots <candidate_hotspots.txt> <distance> <filtered_hotspots.txt>
"""

import sys

out = open(sys.argv[3], 'w')

out.write('chrom'+'\t'+'start'+'\t'+'end'+'\t'+'window_snps'+'\t'+'background_snps'+'\t'+'background_windows'+'\t'+'window_rho'+'\t'+'background_rho'+'\t'+'heat'+'\n')

filtered = []

with open(sys.argv[1], 'r') as f:
	next(f)
	counter = 0
	for line in f:
		chrom = line.split()[0]
		start = line.split()[1]
		end = line.split()[2]
		window_snps = line.split()[3]
		background_snps = line.split()[4]
		background_windows = line.split()[5]
		window_rho = line.split()[6]
		background_rho = line.split()[7]
		heat = line.split()[8]
		
		window = (chrom+'_'+start+'_'+end+'_'+window_snps+'_'+background_snps+'_'+background_windows+'_'+window_rho+'_'+background_rho+'_'+heat)
		
		if counter == 0:
			filtered.append(window)

		window_update = []
		counter = counter + 1
		if counter > 1:
			window_update.append(window)
			
			size = int(end) - int(start)
			midpt = int(end) - size/2
			
# 			print chrom, midpt
			
			last = filtered[-1]
			slast = str(last)
# 			print slast
			


			lchrom = slast.split('_')[0]
# 			print lchrom
# 			lchrom = lchrom.split("'")[1]

			lsize = int(slast.split('_')[2]) - int(slast.split('_')[1])
			lmidpt = int(slast.split('_')[2]) - lsize/2
# 			print lchrom, lmidpt
			lrho = float(slast.split('_')[8])
# 			print lrho

# 			filtered = filtered[:-1] + window_update
			
			
			if lchrom == chrom and abs(midpt - lmidpt) <= int(sys.argv[2]):
				if float(heat) > lrho:
					filtered = filtered[:-1] + window_update
			else:
				filtered.append(window)
			

for h in filtered:
	chrom = h.split('_')[0]
	start = h.split('_')[1]
	end = h.split('_')[2]
	window_snps = h.split('_')[3]
	background_snps = h.split('_')[4]
	background_windows = h.split('_')[5]
	window_rho = h.split('_')[6]
	background_rho = h.split('_')[7]
	heat = h.split('_')[8]

	out.write(chrom+'\t'+start+'\t'+end+'\t'+window_snps+'\t'+background_snps+'\t'+background_windows+'\t'+window_rho+'\t'+background_rho+'\t'+heat+'\n')

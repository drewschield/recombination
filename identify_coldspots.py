"""
identify_coldspots.py <background_rho+gc> <hotspots+gc> <out>
"""

import sys
import decimal
import numpy as np

out = open(sys.argv[3], 'w')
out.write('chrom'+'\t'+'hotspot_start'+'\t'+'hotspot_end'+'\t'+'coldspot_start'+'\t'+'coldspot_end'+'\t'+'distance'+'\t'+'hotspot_heat'+'\t'+'coldspot_heat'+'\t'+'hotspot_gc'+'\t'+'coldspot_gc'+'\n')

backgc_data = []

with open(sys.argv[1], 'r') as background:
	next(background)
	for line in background:
		chrom = line.split()[0]
		start = line.split()[1]
		end = line.split()[2]
		window_rho = line.split()[6]
		back_rho = line.split()[7]
		heat = line.split()[8]
		gc = line.split()[9]
		
		if heat != 'NA':
			if float(back_rho) >= 0.001 and float(back_rho) <= 1:
				if float(heat) >= 0.9 and float(heat) <= 1.1:
					backgc = (chrom+'_'+start+'_'+end+'_'+window_rho+'_'+back_rho+'_'+heat+'_'+gc)
					
					backgc_data.append(backgc)

# sampled = [] # throw coldspots that have already been sampled to not double sample them

with open(sys.argv[2], 'r') as hotspots:
	next(hotspots)
	for line in hotspots:
		chrom = line.split()[0]
		start = int(line.split()[1])
		end = int(line.split()[2])
		window_rho = line.split()[6]
		back_rho = line.split()[7]
		heat = line.split()[8]
		gc = float(line.split()[9])
		
		size = end - start
		midpt = end - size/2
		
		colddist = []
		coldspots = []
		
		for b in backgc_data:
			bchrom = b.split('_')[0]
			bstart = int(b.split('_')[1])
			bend = int(b.split('_')[2])
			brho = b.split('_')[3]
			bbrho = b.split('_')[4]
			bheat = b.split('_')[5]
			bgc = float(b.split('_')[6])
			
			bsize = bend - bstart
			bmidpt = bend - bsize/2
			
			distance = abs(bmidpt - midpt)
			
			cold = (bchrom+'_'+str(bstart)+'_'+str(bend)+'_'+str(distance)+'_'+brho+'_'+bbrho+'_'+bheat+'_'+str(bgc))
			
# 			if cold not in sampled:
			if bchrom == chrom and distance >= 25000:
				if bgc/gc >=0.98 and bgc/gc <=1.02:
					colddist.append(distance)
					coldspots.append(cold)
# 					sampled.append(cold)
		
		if len(colddist) > 1:
		
			mindist = min(colddist)
		
			for c in coldspots:
				count = 0
				if count == 0:
					if int(c.split('_')[3]) == int(mindist):
						out.write(chrom+'\t'+str(start)+'\t'+str(end)+'\t'+c.split('_')[1]+'\t'+c.split('_')[2]+'\t'+c.split('_')[3]+'\t'+heat+'\t'+c.split('_')[6]+'\t'+str(gc)+'\t'+c.split('_')[7]+'\n')
						print chrom, start, end, c.split('_')[3]
						count = count + 1
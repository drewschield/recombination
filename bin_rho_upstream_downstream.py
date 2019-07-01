"""
bin_rho_upstream_downstream.py

Calculate mean, st. dev pop. scaled recombination rate within given distance up and downstream of feature.
Note: integrates numpy with numeric list to get mean, st. dev
Note: requires use of -D b flag when distance file is generated using bedtools closest.

usage: python bin_rho_upstream_downstream.py <distance.in> <binned.out> <updown_distance> <bin_length>
"""

import sys
import numpy as np

out = open(sys.argv[2], 'w')
updown_distance = int(sys.argv[3])
binlen = int(sys.argv[4])

out.write('distance_interval'+'\t'+'total_rho'+'\t'+'total_windows'+'\t'+'mean_rho'+'\t'+'SD_rho'+'\n')

distrho = []

for line in open(sys.argv[1], 'r'):
	dist = line.split()[13]
	rho = line.split()[3]
	distrho.append(dist+'_'+rho)

#get upstream bins
for bin in range(-updown_distance,0,binlen):
	end = bin+binlen
	rec = []
	rhotal = 0
	count = 0
	for d in distrho:
		dist = d.split('_')[0]
		rho = d.split('_')[1]
		if dist != '.':
			if int(dist) >= bin and int(dist) < end:
				if rho != 'NA':
					rhotal = float(rhotal) + float(rho)
					rec.append(rho)
					count = count + 1
#turn list of rho values in bin into numeric (float) array for statistics
	recnum = np.array(rec).astype(np.float)
#calculate statistics per bin
	rmean = np.mean(recnum)
	rstd = np.std(recnum)
	print rmean, rstd
	if count > 0:
		out.write(str(bin)+'\t'+str(rhotal)+'\t'+str(count)+'\t'+str(rmean)+'\t'+str(rstd)+'\n')
	else:
		out.write(str(bin)+'\t'+str(rhotal)+'\t'+str(count)+'\t'+'NA'+'\t'+'NA'+'\n')

#get downstream bins
for bin in range(0,updown_distance,binlen):
	end = bin+binlen
	rec = []
	rhotal = 0
	count = 0
	for d in distrho:
		dist = d.split('_')[0]
		rho = d.split('_')[1]
		if dist != '.':
			if int(dist) >= bin and int(dist) < end:
				if rho != 'NA':
					rhotal = float(rhotal) + float(rho)
					rec.append(rho)
					count = count + 1
#turn list of rho values in bin into numeric (float) array for statistics
	recnum = np.array(rec).astype(np.float)
#calculate statistics per bin
	rmean = np.mean(recnum)
	rstd = np.std(recnum)
	print rmean, rstd
	if count > 0:
		out.write(str(bin)+'\t'+str(rhotal)+'\t'+str(count)+'\t'+str(rmean)+'\t'+str(rstd)+'\n')
	else:
		out.write(str(bin)+'\t'+str(rhotal)+'\t'+str(count)+'\t'+'NA'+'\t'+'NA'+'\n')



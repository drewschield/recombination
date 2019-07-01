import sys

exon_out = open(sys.argv[2], 'w')
intron_out = open(sys.argv[3], 'w')

previous_genename = []
previous_exon = []
previous_start = []
previous_end = []

for line in open(sys.argv[1], 'r'):
	chrom = line.split()[0]
	start = line.split()[3]
	end = line.split()[4]
	strand = line.split()[6]
	name = line.split()[8]
	exon = name.split(':')[2]
	exon = exon.split(';')[0]
	name = name.split(':')[0]
	
	if strand == '+':
		if name != previous_genename:
			exon_out.write(chrom+'\t'+str(start)+'\t'+str(end)+'\t'+name+':exon:'+exon+'\t'+'.'+'\t'+strand+'\n')
# 			print chrom, start, end, strand, name, exon
			previous_exon = exon
			previous_start = start
			previous_end = end
		if name == previous_genename and int(exon) == int(previous_exon) + 1:
# 			print chrom, start, end, strand, name, exon
			intron1_chrom = chrom
			intron1_start = int(previous_end) + 1
			intron1_end = int(start) - 1
			
			intron_out.write(chrom+'\t'+str(intron1_start)+'\t'+str(intron1_end)+'\t'+name+':intron1'+'\t'+'.'+'\t'+strand+'\n')

# 			print chrom, intron1_start, intron1_end, strand, name, 'intron1'


	previous_genename = name

previous_genename = []
previous_exon = []
previous_start = []
previous_end = []

for line in reversed(open(sys.argv[1]).readlines()):
	chrom = line.split()[0]
	start = line.split()[3]
	end = line.split()[4]
	strand = line.split()[6]
	name = line.split()[8]
	exon = name.split(':')[2]
	exon = exon.split(';')[0]
	name = name.split(':')[0]

	if strand == '-':
		if name != previous_genename:
			exon_out.write(chrom+'\t'+str(start)+'\t'+str(end)+'\t'+name+':exon:'+exon+'\t'+'.'+'\t'+strand+'\n')
# 			print chrom, start, end, strand, name, exon
			previous_exon = exon
			previous_start = start
			previous_end = end
			
		if name == previous_genename and (int(exon) == int(previous_exon) + 1 or int(exon) == int(previous_exon) - 1):
# 			print chrom, start, end, strand, name, exon
			intron1_chrom = chrom
			intron1_start = int(start) - 1
			intron1_end = int(previous_end) + 1
			
			intron_out.write(chrom+'\t'+str(intron1_start)+'\t'+str(intron1_end)+'\t'+name+':intron1'+'\t'+'.'+'\t'+strand+'\n')

# 			print chrom, intron1_start, intron1_end, strand, name, 'intron1'

	previous_genename = name

# 	if strand == '-':
# 		if 
# 	else:
# 		print 'reverse'
		
# 	previous_exon = exon	
	
# leverage reverse order of exon numbers for reverse strand genes
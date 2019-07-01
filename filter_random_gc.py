import sys

out = open(sys.argv[2], 'w')

for line in open(sys.argv[1], 'r'):
	if float(line.split()[3]) >= 0.3812458 and float(line.split()[3]) <= 0.3968068:
		out.write(line) 
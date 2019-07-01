pop=$1
snps=$2
bpen=$3
touch $pop/temp.txt
for scaff in `cat chrom.list`
do
	cat $pop/$pop.$scaff.$snps.$bpen.windowed.10Kb.r.txt >> $pop/temp.txt
done
awk '!seen[$1,$2,$3,$4,$5,$6,$7]++' $pop/temp.txt > $pop/$pop.$snps.$bpen.windowed.10Kb.r.txt


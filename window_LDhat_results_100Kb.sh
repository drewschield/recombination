pop=$1
snps=$2
bpen=$3
for scaff in `cat chrom.list`
do
	echo calculating windowed statistics for $scaff
	python window_ldhat_r_v1.1.py _chrom_100Kb/$scaff.100Kb.window.bed $pop/$scaff.$snps.$bpen.res.txt $pop/$pop.$scaff.$snps.$bpen.windowed.100Kb.r.txt
done


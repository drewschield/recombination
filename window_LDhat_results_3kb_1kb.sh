pop=$1
snps=$2
bpen=$3
for scaff in `cat chrom.list`
do
	echo calculating windowed statistics for $scaff
	python window_ldhat_r_v1.1.py _chrom_3kb_1kb/$scaff.3kb_1kb.window.bed $pop/$scaff.$snps.$bpen.res.txt $pop/$pop.$scaff.$snps.$bpen.windowed.3kb_1kb.r.txt
done


pop=$1
snps=$2
lk=$3
its=$4
samp=$5
bpen=$6
burn=$7
cd $pop
for scaff in `cat ../chrom.list`
do
	../LDhat/interval -seq ../../LDhat_input/$pop/$pop.$scaff.$snps.snps.ldhat.sites -loc ../../LDhat_input/$pop/$pop.$scaff.$snps.snps.ldhat.locs -lk $lk -its $its -samp $samp -bpen $bpen
	mv rates.txt $scaff.$snps.$bpen.rates.txt
	mv bounds.txt $scaff.$snps.$bpen.bounds.txt
	mv new_lk.txt lk.$scaff.$snps
	../LDhat/stat -input $scaff.$snps.$bpen.rates.txt -burn $burn -loc ../../LDhat_input/$pop/$pop.$scaff.$snps.snps.ldhat.locs
	mv res.txt $scaff.$snps.$bpen.res.txt
done

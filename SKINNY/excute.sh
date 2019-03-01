for((i=0;i<64;i++)); do 
	python3 Skinny.py $1 ${i} > cvc/${i}.cvc & 
done

for job in `jobs -p`; do
 wait $job
done

for((i=0;i<64;i++)); do 
  stp cvc/${i}.cvc --cryptominisat --threads 2 > cvc/res/${i}.res & 
done

for job in `jobs -p`; do
 wait $job
done

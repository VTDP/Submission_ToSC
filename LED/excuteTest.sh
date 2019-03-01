for((i=0;i<64;i++)); do 
  stp Test/${i}.cvc --cryptominisat --threads 2 > Test/res/${i}.res & 
done

  for job in `jobs -p`; do
        wait $job
  done




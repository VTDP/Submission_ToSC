for((i=$1;i<$2;i++)); do 
    python3 LED.py 7  $i > cvc_test/${i}.cvc & 
done

for job in `jobs -p`; do
     wait $job
done


for((i=$1;i<$2;i++)); do 
  stp cvc_test/${i}.cvc --cryptominisat --threads 4 > cvc_test/res/${i}.res & 
done




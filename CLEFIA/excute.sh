for((i=$1;i<$2;i++)); do 
    python3 CLEFIA.py 10 $i > cvc/$i.cvc
done

for job in `jobs -p`; do
     wait $job
done

for((i=$1;i<$2;i++)); do
   nohup stp cvc/$i.cvc --cryptominisat --threads 4 > cvc/res/$i.res &
done

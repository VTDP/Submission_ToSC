for((i=0;i<16;i++)); do 
    python3 Misty.py 6 ${i} > cvc_less/${i}.cvc & 
done

for job in `jobs -p`; do
    wait $job
done

for((i=0;i<16;i++)); do 
    nohup stp cvc_less/${i}.cvc --cryptominisat --threads 4 > cvc_less/res/${i}.res & 

    for job in `jobs -p`; do
        wait $job
    done
done

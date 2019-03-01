for((i=0;i<128;i++)); do 
    nohup python3 Camellia.py 7 6 ${i} > cvc/${i}.cvc & 
    for job in `jobs -p`; do
        wait $job
    done
    nohup stp cvc/${i}.cvc --cryptominisat --threads 8 > cvc/res/${i}.res & 

    for job in `jobs -p`; do
        wait $job
    done

    rm cvc/${i}.cvc
done

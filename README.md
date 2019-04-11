# submission_for_ToSC
Some source codes about the submitted paper to ToSC 2019 Issuse 1

Usage:
For example, to search for the division property of 7-Round LED with the 0 bit of ciphertexts, with 63 active bits

cd LED/
# 7 for round and 0 for the position of ciphertext bit
python3 LED.py 7 0 > cvc_0.cvc 
# if the result is valid, the bit is balanced, otherwise, not balanced
stp cvc_0.cvc --cryptominisat --threads 4 > res_0.res





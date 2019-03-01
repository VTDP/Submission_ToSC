# submission_for_ToSC
Some source codes about the submitted paper to ToSC 2019 Issuse 1

Usage:
For example, 7-Round LED,  the 0 bit of ciphertexts, with 63 active bits

cd LED/
python3 LED.py 7 0 > cvc_0.cvc 
stp cvc_0.cvc --cryptominisat --threads 4 > res_0.res



from Camellia_base import *
from Const import *
import sys

inVec =  [ x for x in range(1, 128)] 
outVec = [0]

#r = int( sys.argv[1] )
#mid = int( sys.argv[2] )
# FL/FL^-1 is placed after the first six round
mid = 6

came = Camellia( "P_Matrix", P, 'Pinv_Matrix', P_inv,  'MatName_FL', FL, 'MatName_FL_inv', FL_inv, 
        'Sbox', sbox, 8, 8, 
        128, 7,  mid, inVec, outVec )

print ( '\n'.join( came.getConstrs () ) )

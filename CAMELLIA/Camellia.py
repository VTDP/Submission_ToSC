from Camellia_base import *
from Const import *
import sys

inVec =  [ x for x in range(64, 64+50)] 
outVec = [ int ( sys.argv[3] )]

r = int( sys.argv[1] )
mid = int( sys.argv[2] )

came = Camellia( "P_Matrix", P, 'Pinv_Matrix', P_inv,  'MatName_FL', FL, 'MatName_FL_inv', FL_inv, 
        'Sbox', sbox, 8, 8, 
        128, r,  mid, inVec, outVec )

print ( '\n'.join( came.getConstrs () ) )

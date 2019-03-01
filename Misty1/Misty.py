from Misty_base import *
from Const import *

    #  def _init__(self,  matNameFL, matrixFL,
    #                     matNameFO, matrixFO,
    #                     matNameFI_zero_extended, matrixFI_zero_extended,
    #                     matNameFI_truncate, matrixFI_truncate,
    #                     sboxName9, sbox9, sboxDim9, numberOfSbox9,
    #                     sboxName7, sbox7, sboxDim7, numberOfSbox7,
    #                     dim,
    #                     r,
    #                     inVec, outVec ):
#inVec =[ 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
#         32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
inVec = [ x for x in range(2,64)]
outVec = [ int( sys.argv[2] ) ]
misty = Misty( 'MatrixFL', matrixFL, 'Matrix_FL_1', matrix_FL_1, 
    'MatrixFO', matrixFO,   
    'MatrixFI_zero_ext', matrix_FI_extended, 
    'MatrixFI_truncate', matrix_FI_truncate, 
    'SBOX9', s9, 9, 6,
    'SBOX7', s7, 7, 3, 
     64, 
     int(sys.argv[1]), 
     inVec, outVec )
  
print( '\n'.join( misty.getConstrs() ) )

#for s in misty.getConstrs():
#    print ( s )
#    if s == None:
#        input()
        

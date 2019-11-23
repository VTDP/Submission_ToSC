from Misty_base import *
from Const import *

inVec = [ x for x in range(1,64)]
outVec = [0 ]
misty = Misty( 'MatrixFL', matrixFL,  
    'MatrixFO', matrixFO,   
    'MatrixFI_zero_ext', matrix_FI_extended, 
    'MatrixFI_truncate', matrix_FI_truncate, 
    'SBOX9', s9, 9, 6,
    'SBOX7', s7, 7, 3, 
     64, 
     7, 
     inVec, outVec )
  
print( '\n'.join( misty.getConstrs() ) )

#for s in misty.getConstrs():
#    print ( s )
#    if s == None:
#        input()
        


from CLEFIA_base import *
from Constant import *

inVec = [ x for x in range(1,128)]
outVec = [0 ]

clefia = CLEFIA( 'CLEFIA_S0', S0, 8, 4,
                 'CLEFIA_S1', S1, 8, 4,
                 'CLEFIA_M0', M0, 
                 'CLEFIA_M1', M1, 
                 128, 10, inVec, outVec )
print( '\n'.join( clefia.getConstrs() ) )


from AssertSbox import *
from Matrix import *
import sys

class Skinny(object):
    def __init__(self, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
        self.__sbox = AssertSbox(sboxName, sbox, sboxDim, r, numberOfSbox)
        self.__matName = matName
        self.__matrix = matrix
        self.__sboxDim = sboxDim
        self.__dim = dim
        self.__round = r
        self.__constrs = []
        self.__variables = self.__declareVariables()
        self.__afterSboxVariables = self.__declareSboxVariables()
        self.__constrs += self.__sbox.get_asserts_declares()
        self.__gen_round_constrs()
        self.__gen_init_constrs(inVec, outVec)
        
    def __declareVariables(self):
        # declare the round variables
        variables = [ [0 for x in range(self.__dim)] 
                for x in range(self.__round + 1) ]
        for r in range(self.__round + 1):
            for p in range(self.__dim):
                s = 'SKINNY_X_%d_%d' % (r, p)
                variables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.__constrs.append(s)
        return variables

    def __declareSboxVariables(self):
        afterSboxVariables = [ [0 for x in range(self.__dim)] 
                for x in range(self.__round) ]
        for r in range(self.__round):
            for p in range(self.__dim):
                s = 'SKINNY_SBOX_%d_%d' % (r, p)
                afterSboxVariables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.__constrs.append(s)
        return afterSboxVariables
    
    def __gen_round_constrs(self):
        # pass sbox
        for r in range(self.__round):
            for p in range( int(self.__dim/ self.__sboxDim) ):
                self.__constrs.append( self.__sbox.build_constrs(
                self.__variables[r][4 * p: 4*(p+1)], 
                self.__afterSboxVariables[r][4*p:4*(p+1)],
                r,p ),
                )
                
        # pass shiftRows and MixColumn
            # 0  1  2  3             0  1  2  3 
            # 4  5  6  7   ----->    7  4  5  6
            # 8  9  10 11            10 11 8  9
            # 12 13 14 15            13 14 15 12
            
            inVec0 = self.__afterSboxVariables[r][0:4]   +   self.__afterSboxVariables[r][28:32] + self.__afterSboxVariables[r][40:44] + self.__afterSboxVariables[r][52:56]
            inVec1 = self.__afterSboxVariables[r][4:8]   +   self.__afterSboxVariables[r][16:20] + self.__afterSboxVariables[r][44:48] + self.__afterSboxVariables[r][56:60]
            inVec2 = self.__afterSboxVariables[r][8:12]  +  self.__afterSboxVariables[r][20:24] + self.__afterSboxVariables[r][32:36] + self.__afterSboxVariables[r][60:64]
            inVec3 = self.__afterSboxVariables[r][12:16] + self.__afterSboxVariables[r][24:28] + self.__afterSboxVariables[r][36:40] + self.__afterSboxVariables[r][48:52]

            outVec0 = self.__variables[r+1][0:4]   +   self.__variables[r+1][16:20] + self.__variables[r+1][32:36] + self.__variables[r+1][48:52]
            outVec1 = self.__variables[r+1][4:8]   +   self.__variables[r+1][20:24] + self.__variables[r+1][36:40] + self.__variables[r+1][52:56]
            outVec2 = self.__variables[r+1][8:12]  +  self.__variables[r+1][24:28] + self.__variables[r+1][40:44] + self.__variables[r+1][56:60]
            outVec3 = self.__variables[r+1][12:16] + self.__variables[r+1][28:32] + self.__variables[r+1][44:48] + self.__variables[r+1][60:64]
            
            #m = Matrix(matrixName, L, inVec1, outVec1, 0, 1)
            m = Matrix(self.__matName, self.__matrix, inVec0, outVec0, r, 0 )
            self.__constrs += m.get_declares_asserts()

            m = Matrix(self.__matName, self.__matrix, inVec1, outVec1, r, 1 )
            self.__constrs += m.get_declares_asserts() 

            m = Matrix(self.__matName, self.__matrix, inVec2, outVec2, r, 2 )
            self.__constrs += m.get_declares_asserts() 

            m = Matrix(self.__matName, self.__matrix, inVec3, outVec3, r, 3 )
            self.__constrs += m.get_declares_asserts() 

    def __gen_init_constrs(self, constants, tail):
        for i in range(self.__dim):
            if i in constants:
                self.__constrs.append( 'ASSERT %s = 0bin1;' % self.__variables[0][i])
            else:
                self.__constrs.append( 'ASSERT %s = 0bin0;' % self.__variables[0][i])

        for i in range(self.__dim):
            if i in tail:
                self.__constrs.append( 'ASSERT %s = 0bin1;' % self.__variables[self.__round][i])
            else:
                self.__constrs.append( 'ASSERT %s = 0bin0;' % self.__variables[self.__round][i])
        self.__constrs.append( 'QUERY FALSE;')
        #self.__constrs.append( 'COUNTEREXAMPLE;')

    def getConstrs(self):
        return self.__constrs
        


    
def main():
    sbox = [0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf]
    matrix = [[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]
    #inVec = [0,1,2,3, 20,21,22,23, 40,41,42,43, 60,61,62,63 ] 
    #inVec = [ x for x in range(0, 48) ] + [ x for x in range(52, 64) ]
    inVec = [ x for x in range(4, 64 ) ]
    outVec = [ int( sys.argv[2] ) ] 
#def __init__(self, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
    skinny = Skinny('SKINNYMAT', matrix, 'SKINNYSBOX', sbox, 4, 64, int(sys.argv[1] ),16, inVec, outVec)
    print( '\n'.join( skinny.getConstrs() ) )


if __name__ == '__main__':
    main()

                


                
                






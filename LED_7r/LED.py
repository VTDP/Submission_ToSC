from AssertSbox import *
from Matrix import *
import sys

class AES(object):
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

    def __bin(self, num, length ):
        return '0bin' + bin(num)[2:].zfill(length)
        
    def __declareVariables(self):
        # declare the round variables
        variables = [ [0 for x in range(self.__dim)] 
                for x in range(self.__round + 1) ]
        for r in range(self.__round + 1):
            for p in range(self.__dim):
                s = 'AES_X_%d_%d' % (r, p)
                variables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.__constrs.append(s)
        return variables

    def __declareSboxVariables(self):
        afterSboxVariables = [ [0 for x in range(self.__dim)] 
                for x in range(self.__round) ]
        for r in range(self.__round):
            for p in range(self.__dim):
                s = 'AES_SBOX_%d_%d' % (r, p)
                afterSboxVariables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.__constrs.append(s)
        return afterSboxVariables
    
    def __gen_round_constrs(self):
        '''
        constraints for model
        '''
        
        # pass sbox
        for r in range(self.__round):
            for p in range( int(self.__dim/ self.__sboxDim) ):
                self.__constrs.append( self.__sbox.build_constrs(
                    self.__variables[r][self.__sboxDim * p: self.__sboxDim*(p+1)], 
                    self.__afterSboxVariables[r][self.__sboxDim*p:self.__sboxDim*(p+1)],
                    r,p ),
                    )
        # pass shiftRows and MixColumn
            # 0  1  2  3             0  1  2  3 
            # 4  5  6  7   ----->    5  6  7  4
            # 8  9  10 11            10 11 8  9
            # 12 13 14 15            15 12 13 14
            inVec0 = self.__afterSboxVariables[r][0:self.__sboxDim]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 5 : self.__sboxDim * 6 ]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 10: self.__sboxDim * 11]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 15: self.__sboxDim * 16]
            inVec1 = self.__afterSboxVariables[r][self.__sboxDim * 1: self.__sboxDim * 2] \
                    +self.__afterSboxVariables[r][self.__sboxDim * 6: self.__sboxDim * 7]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 11:self.__sboxDim * 12]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 12:self.__sboxDim * 13]
            inVec2 = self.__afterSboxVariables[r][self.__sboxDim * 2 :self.__sboxDim * 3] \
                    +self.__afterSboxVariables[r][self.__sboxDim * 7: self.__sboxDim * 8] \
                    +self.__afterSboxVariables[r][self.__sboxDim * 8 :self.__sboxDim * 9] \
                    +self.__afterSboxVariables[r][self.__sboxDim * 13: self.__sboxDim *14]
            inVec3 = self.__afterSboxVariables[r][self.__sboxDim * 3: self.__sboxDim * 4]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 4:self.__sboxDim * 5] \
                    +self.__afterSboxVariables[r][self.__sboxDim * 9: self.__sboxDim * 10]\
                    +self.__afterSboxVariables[r][self.__sboxDim * 14: self.__sboxDim * 15]

            outVec0 = self.__variables[r+1][self.__sboxDim * 0: self.__sboxDim * 1]\
                  +   self.__variables[r+1][self.__sboxDim * 4: self.__sboxDim * 5]\
                  +   self.__variables[r+1][self.__sboxDim * 8: self.__sboxDim * 9]\
                  +   self.__variables[r+1][self.__sboxDim * 12: self.__sboxDim * 13]
            outVec1 = self.__variables[r+1][self.__sboxDim * 1: self.__sboxDim * 2]\
                  +   self.__variables[r+1][self.__sboxDim * 5: self.__sboxDim * 6]\
                  +   self.__variables[r+1][self.__sboxDim * 9: self.__sboxDim * 10]\
                  +   self.__variables[r+1][self.__sboxDim * 13: self.__sboxDim * 14]
            outVec2 = self.__variables[r+1][self.__sboxDim * 2: self.__sboxDim * 3]\
                  +   self.__variables[r+1][self.__sboxDim * 6: self.__sboxDim * 7]\
                  +   self.__variables[r+1][self.__sboxDim * 10: self.__sboxDim * 11]\
                  +   self.__variables[r+1][self.__sboxDim * 14: self.__sboxDim * 15]
            outVec3 = self.__variables[r+1][self.__sboxDim * 3: self.__sboxDim * 4]\
                  +   self.__variables[r+1][self.__sboxDim * 7: self.__sboxDim * 8]\
                  +   self.__variables[r+1][self.__sboxDim * 11: self.__sboxDim * 12]\
                  +   self.__variables[r+1][self.__sboxDim * 15: self.__sboxDim * 16]

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

        # C_0 + C_1 + ... + C_63 = 0
        s = 'ASSERT BVPLUS(10, 0bin000000000@%s ' % self.__variables[self.__round][0]
        for i in range(1, 64):
            s += ', 0bin000000000@%s' % self.__variables[self.__round][i]  
        s += ') = 0bin0000000001;'
        self.__constrs.append( s ) 
        self.__constrs.append( 'QUERY FALSE;')
        #self.__constrs.append( 'COUNTEREXAMPLE;' )

    def getConstrs(self):
        return self.__constrs
    
def main():
    sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
    matrix = [
        [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], \
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0], \
        [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0], \
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], \
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0], \
        [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1], \
        [0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1], \
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0], \
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1], \
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0], \
        [1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0], \
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1], \
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1], \
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0], \
        [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1], \
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1]]

    inVec = [ 0,1,2,3,      4,5,6,       8,9,10,11,    12,13,14,15,
              16,17,18,19,  20,21,22,23, 24,25,26,27,  28,29,30,31, 
              32,33,34,35,  36,37,38,39, 40,41,42,43,  44,45,46,47, 
              48,49,50,51,  52,53,54,55, 56,57,58,59,  60,61,62,63 ]
    outVec = [ 0 ] 
    skinny = AES('LEDMAT', matrix, 'LEDSBOX', sbox, 4, 64, 1, 16, inVec, outVec)
    print( '\n'.join( skinny.getConstrs() ) )


if __name__ == '__main__':
    main()

                


                
                






from AssertSbox import *
from Matrix import *
from constant import *
from Matrix_non_square import *
import sys

class AES(object):
    def __init__(self, firstName, firstMatrix, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
        self.__sbox = AssertSbox(sboxName, sbox, sboxDim, r, numberOfSbox)
        self.__firstName = firstName
        self.__firstMatrix = firstMatrix
        self.__matName = matName
        self.__matrix = matrix
        self.__sboxDim = sboxDim
        self.__dim = dim
        self.__round = r
        self.__constrs = []
        self.__variables = self.__declareVariables()
        self.__var2 = self.__declareVariables2()
        self.__afterSboxVariables = self.__declareSboxVariables()
        self.__constrs += self.__sbox.get_asserts_declares()
        self.__gen_round_constrs()
        self.__gen_init_constrs(inVec, outVec)
        
    def __declareVariables(self):
        # declare the round variables
        variables = [ [0 for x in range(self.__dim) ] 
                for x in range(self.__round + 1) ]
        for r in range(self.__round + 1):
            for p in range(self.__dim):
                s = 'AES_X_%d_%d' % (r, p)
                variables[r][p] = s
                s = '%s:BITVECTOR(1);' % s
                self.__constrs.append(s)
        return variables

    def __declareVariables2(self):
        # declare the input variables of the distinguishers
        var2 = [0 for x in range(self.__dim)] 

        for p in range(self.__dim):
            s = 'AES_SX_%d' % ( p)
            var2[p] = s
            s = '%s:BITVECTOR(1);' % s
            self.__constrs.append(s)
        return var2

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
        inVec0 = self.__var2[0 * self.__sboxDim: 1 * self.__sboxDim]\
               + self.__var2[4 * self.__sboxDim: 5 * self.__sboxDim]\
               + self.__var2[8 * self.__sboxDim: 9 * self.__sboxDim]

        inVec1 = self.__var2[1 * self.__sboxDim: 2 * self.__sboxDim]\
               + self.__var2[5 * self.__sboxDim: 6 * self.__sboxDim]\
               + self.__var2[9 * self.__sboxDim: 10 * self.__sboxDim]\
               + self.__var2[13 * self.__sboxDim: 14 * self.__sboxDim]

        inVec2 = self.__var2[2 * self.__sboxDim: 3 * self.__sboxDim]\
               + self.__var2[6 * self.__sboxDim: 7 * self.__sboxDim]\
               + self.__var2[10 * self.__sboxDim: 11 * self.__sboxDim]\
               + self.__var2[14 * self.__sboxDim: 15 * self.__sboxDim]

        inVec3 = self.__var2[3 * self.__sboxDim: 4 * self.__sboxDim]\
               + self.__var2[7 * self.__sboxDim: 8 * self.__sboxDim]\
               + self.__var2[11 * self.__sboxDim: 12 * self.__sboxDim]\
               + self.__var2[15 * self.__sboxDim: 16 * self.__sboxDim]

        outVec0 = self.__variables[0][0 * self.__sboxDim: 1 * self.__sboxDim]\
                   + self.__variables[0][4 * self.__sboxDim: 5 * self.__sboxDim]\
                   + self.__variables[0][8 * self.__sboxDim: 9 * self.__sboxDim]\
                   + self.__variables[0][12 * self.__sboxDim: 13 * self.__sboxDim]

        outVec1 = self.__variables[0][1 * self.__sboxDim: 2 * self.__sboxDim]\
                   + self.__variables[0][5 * self.__sboxDim: 6 * self.__sboxDim]\
                   + self.__variables[0][9 * self.__sboxDim: 10 * self.__sboxDim]\
                   + self.__variables[0][13 * self.__sboxDim: 14 * self.__sboxDim]

        outVec2 = self.__variables[0][2 * self.__sboxDim: 3 * self.__sboxDim]\
                   + self.__variables[0][6 * self.__sboxDim: 7 * self.__sboxDim]\
                   + self.__variables[0][10 * self.__sboxDim: 11 * self.__sboxDim]\
                   + self.__variables[0][14 * self.__sboxDim: 15 * self.__sboxDim]

        outVec3 = self.__variables[0][3 * self.__sboxDim: 4 * self.__sboxDim]\
                   + self.__variables[0][7 * self.__sboxDim: 8 * self.__sboxDim]\
                   + self.__variables[0][11 * self.__sboxDim: 12 * self.__sboxDim]\
                   + self.__variables[0][15 * self.__sboxDim: 16 * self.__sboxDim]

        m = NonSquareMatrix(self.__firstName, self.__firstMatrix, inVec0, outVec0, 10, 0 )
        self.__constrs += m.get_declares_asserts()

        m = Matrix(self.__matName, self.__matrix, inVec1, outVec1, 10, 1 )
        self.__constrs += m.get_declares_asserts()

        m = Matrix(self.__matName, self.__matrix, inVec2, outVec2, 10, 2 )
        self.__constrs += m.get_declares_asserts()

        m = Matrix(self.__matName, self.__matrix, inVec3, outVec3, 10, 3 )
        self.__constrs += m.get_declares_asserts()

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
                self.__constrs.append( 'ASSERT %s = 0bin1;' % self.__var2[i])
            else:
                self.__constrs.append( 'ASSERT %s = 0bin0;' % self.__var2[i])

        s = 'ASSERT BVPLUS(10, 0bin000000000@%s ' % self.__variables[self.__round][0]
        for i in range(1, self.__dim):
            s += ', 0bin000000000@%s' % self.__variables[self.__round][i]  
        s += ') = 0bin0000000001;'
        self.__constrs.append( s ) 
        self.__constrs.append( 'QUERY FALSE;')
        self.__constrs.append( 'COUNTEREXAMPLE;')

    def getConstrs(self):
        return self.__constrs
    
def main():
    inVec = [x for x in range(0, 96)] + [ x for x in range(104, 128)]
    outVec = [ 0 ] 
#def __init__(self, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
    aes = AES('FIRST', first, 'AESMAT', matrix, 'AESSBOX', invSbox, 8, 128, 4, 16, inVec, outVec)
    print( '\n'.join( aes.getConstrs() ) )



if __name__ == '__main__':
    main()

                


                
                






from AssertSbox import *
from Matrix import *
from constant import *
from Matrix_non_square import *
import sys

class AES(object):
    def __init__(self,fname, f, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
        self.__sbox = AssertSbox(sboxName, sbox, sboxDim, r, numberOfSbox)
        self.__firstMatrixName = fname
        self.__firstMatrix = f
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
        # pass sbox
        for r in range(self.__round):
            if r == 0:
                # r == 0, apply the first matrix
                inVec0 = self.__variables[r][0 * self.__sboxDim: 1 * self.__sboxDim]\
                       + self.__variables[r][4 * self.__sboxDim: 5 * self.__sboxDim]\
                       + self.__variables[r][8 * self.__sboxDim: 9 * self.__sboxDim]

                inVec1 = self.__variables[r][1 * self.__sboxDim: 2 * self.__sboxDim]\
                       + self.__variables[r][5 * self.__sboxDim: 6 * self.__sboxDim]\
                       + self.__variables[r][9 * self.__sboxDim: 10 * self.__sboxDim]

                inVec2 = self.__variables[r][2 * self.__sboxDim: 3 * self.__sboxDim]\
                       + self.__variables[r][6 * self.__sboxDim: 7 * self.__sboxDim]\
                       + self.__variables[r][10 * self.__sboxDim: 11 * self.__sboxDim]

                inVec3 = self.__variables[r][3 * self.__sboxDim: 4 * self.__sboxDim]\
                       + self.__variables[r][7 * self.__sboxDim: 8 * self.__sboxDim]\
                       + self.__variables[r][11 * self.__sboxDim: 12 * self.__sboxDim]
            else:
                inVec0 = self.__variables[r][0 * self.__sboxDim: 1 * self.__sboxDim]\
                       + self.__variables[r][4 * self.__sboxDim: 5 * self.__sboxDim]\
                       + self.__variables[r][8 * self.__sboxDim: 9 * self.__sboxDim]\
                       + self.__variables[r][12 * self.__sboxDim: 13 * self.__sboxDim]

                inVec1 = self.__variables[r][1 * self.__sboxDim: 2 * self.__sboxDim]\
                       + self.__variables[r][5 * self.__sboxDim: 6 * self.__sboxDim]\
                       + self.__variables[r][9 * self.__sboxDim: 10 * self.__sboxDim]\
                       + self.__variables[r][13 * self.__sboxDim: 14 * self.__sboxDim]

                inVec2 = self.__variables[r][2 * self.__sboxDim: 3 * self.__sboxDim]\
                       + self.__variables[r][6 * self.__sboxDim: 7 * self.__sboxDim]\
                       + self.__variables[r][10 * self.__sboxDim: 11 * self.__sboxDim]\
                       + self.__variables[r][14 * self.__sboxDim: 15 * self.__sboxDim]\

                inVec3 = self.__variables[r][3 * self.__sboxDim: 4 * self.__sboxDim]\
                       + self.__variables[r][7 * self.__sboxDim: 8 * self.__sboxDim]\
                       + self.__variables[r][11 * self.__sboxDim: 12 * self.__sboxDim]\
                       + self.__variables[r][15 * self.__sboxDim: 16 * self.__sboxDim]

            outVec0 = self.__afterSboxVariables[r][0 * self.__sboxDim: 1 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][4 * self.__sboxDim: 5 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][8 * self.__sboxDim: 9 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][12 * self.__sboxDim: 13 * self.__sboxDim]

            outVec1 = self.__afterSboxVariables[r][1 * self.__sboxDim: 2 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][5 * self.__sboxDim: 6 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][9 * self.__sboxDim: 10 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][13 * self.__sboxDim: 14 * self.__sboxDim]

            outVec2 = self.__afterSboxVariables[r][2 * self.__sboxDim: 3 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][6 * self.__sboxDim: 7 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][10 * self.__sboxDim: 11 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][14 * self.__sboxDim: 15 * self.__sboxDim]

            outVec3 = self.__afterSboxVariables[r][3 * self.__sboxDim: 4 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][7 * self.__sboxDim: 8 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][11 * self.__sboxDim: 12 * self.__sboxDim]\
                   + self.__afterSboxVariables[r][15 * self.__sboxDim: 16 * self.__sboxDim]

            if r == 0:
                matName = self.__firstMatrixName
                mat = self.__firstMatrix
                m = NonMatrix(matName, mat, inVec0, outVec0, r, 0 )
                self.__constrs += m.get_declares_asserts()

                m = NonMatrix(matName, mat, inVec1, outVec1, r, 1 )
                self.__constrs += m.get_declares_asserts() 

                m = NonMatrix(matName, mat, inVec2, outVec2, r, 2 )
                self.__constrs += m.get_declares_asserts() 

                m = NonMatrix(matName, mat, inVec3, outVec3, r, 3 )
                self.__constrs += m.get_declares_asserts() 
            else:
                matName = self.__matName
                mat = self.__matrix

                m = Matrix(matName, mat, inVec0, outVec0, r, 0 )
                self.__constrs += m.get_declares_asserts()

                m = Matrix(matName, mat, inVec1, outVec1, r, 1 )
                self.__constrs += m.get_declares_asserts() 

                m = Matrix(matName, mat, inVec2, outVec2, r, 2 )
                self.__constrs += m.get_declares_asserts() 

                m = Matrix(matName, mat, inVec3, outVec3, r, 3 )
                self.__constrs += m.get_declares_asserts() 

            for p in range(4):
                self.__constrs.append( self.__sbox.build_constrs(
                    self.__afterSboxVariables[r][self.__sboxDim * p: self.__sboxDim*(p+1)], 
                    self.__variables[r + 1][self.__sboxDim*p:self.__sboxDim*(p+1)],
                    r,p ),
                    )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 7: self.__sboxDim* 8 ], 
                self.__variables[r + 1][self.__sboxDim* 4: self.__sboxDim* 5],
                r, 4 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 4: self.__sboxDim* 5 ], 
                self.__variables[r + 1][self.__sboxDim* 5: self.__sboxDim* 6],
                r, 5 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 5: self.__sboxDim* 6 ], 
                self.__variables[r + 1][self.__sboxDim* 6: self.__sboxDim* 7],
                r, 6 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 6: self.__sboxDim* 7 ], 
                self.__variables[r + 1][self.__sboxDim* 7: self.__sboxDim* 8],
                r, 7),
                )

            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 10: self.__sboxDim* 11 ], 
                self.__variables[r + 1][self.__sboxDim* 8: self.__sboxDim* 9],
                r, 8 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 11: self.__sboxDim* 12 ], 
                self.__variables[r + 1][self.__sboxDim* 12: self.__sboxDim* 13],
                r, 9 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 8: self.__sboxDim* 9 ], 
                self.__variables[r + 1][self.__sboxDim* 10: self.__sboxDim* 11],
                r, 10 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 9: self.__sboxDim* 10 ], 
                self.__variables[r + 1][self.__sboxDim* 11: self.__sboxDim* 12],
                r, 11 ),
                )

            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 13: self.__sboxDim* 14 ], 
                self.__variables[r + 1][self.__sboxDim* 12: self.__sboxDim* 13],
                r, 12 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 14: self.__sboxDim* 15 ], 
                self.__variables[r + 1][self.__sboxDim* 13: self.__sboxDim* 14],
                r, 13 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 15: self.__sboxDim* 16 ], 
                self.__variables[r + 1][self.__sboxDim* 14: self.__sboxDim* 15],
                r, 14 ),
                )
            self.__constrs.append( self.__sbox.build_constrs(
                self.__afterSboxVariables[r][self.__sboxDim * 12: self.__sboxDim* 13 ], 
                self.__variables[r + 1][self.__sboxDim* 15: self.__sboxDim* 16],
                r, 15 ),
                )

    def __gen_init_constrs(self, constants, tail):
        for i in range(self.__dim):
            if i in constants:
                self.__constrs.append( 'ASSERT %s = 0bin1;' % self.__variables[0][i])
            else:
                self.__constrs.append( 'ASSERT %s = 0bin0;' % self.__variables[0][i])

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
    inVec = [x for x in range(8)] + [ x for x in range(32, 40)] + [ x for x in range(64, 72) ]
    outVec = [ 0 ] 
#def __init__(self, matName, matrix, sboxName, sbox, sboxDim,dim, r, numberOfSbox, inVec, outVec):
    aes = AES('FIRST', first, 'AESMAT', matrix, 'AESSBOX', invSbox, 8, 128, int(sys.argv[1] ), 16, inVec, outVec)
    print( '\n'.join( aes.getConstrs() ) )


if __name__ == '__main__':
    main()

                


                
                






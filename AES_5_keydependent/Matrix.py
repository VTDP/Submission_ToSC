class Matrix(object):
    '''
    a class to generate the constriants for input u and output v
    the static variable @define indicate that we have declared the matrix M and indentitty matrix E 
    '''
    define = False

    def __init__(self, matrixName, matrix,inVec, outVec,  r, p):
        '''
        @matrixMame: a string naming M
        @matrix: a two-fold list standing for M
        @inVec: a list of input variables
        @outVec: a list of output variables

        @return: a set of constraints on inVec and outVec
        '''
        self._matrixName = '%s' % matrixName 
        self._matrix = matrix
        self._inVec = inVec
        self._outVec = outVec
        self._dim = len(inVec)

        # generate the indentity matrix
        self._resMatrix = [ [ 0 for x in range(self._dim) ] for x in range(self._dim) ]
        for i in range(self._dim):
            for j in range(self._dim):
                if i == j:
                    self._resMatrix[i][j] = 1
                else:
                    self._resMatrix[i][j] = 0

        self._declares = []
        self._asserts = []
        # the auxiliary matrix M^{\expand'}_{v, u}
        self._invMatName = 'inv_%d_%d'%(r, p)
        # E
        self._resMatName = 'res'

        self.__declareMatrix()
        self.__declare_temp_matrix_invMatrix()
        self.__genHammingConstrs()

    def __bin(self, num, length ):
        return '0bin' + bin(num)[2:].zfill(length)

    def __genHammingConstrs(self):
        '''
        asserts the hamming weights of input vector and that of output vector are equal
        \sum_{i=0}^{n-1} u_i = \sum_{i=0}^{n-1} v_i
        ''' 

        s = 'ASSERT BVPLUS(%d'% self._dim  
        for i in range(self._dim):
            s += ', %s@%s' % (self.__bin(0, self._dim - 1 ), self._inVec[i] )
        s += ')'

        s += ' = BVPLUS(%d'% self._dim
            
        for i in range(self._dim):
            s += ', %s@%s' % (self.__bin(0, self._dim - 1 ), self._outVec[i] )
        s += ');'
        self._declares.append( s )

    def __declareMatrix(self):
        '''
        declare M and E
        in this paper, a cipher only takes one kind of matrix, so we just declare them only once
        '''
        if Matrix.define==False: 
            s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                    self._matrixName, 2 * self._dim, 1 )
            self._declares.append(s)

            for row in range(self._dim):
                for col in range(self._dim):
                    s = 'ASSERT %s[%s@%s]=%s;' %( 
                            self._matrixName, 
                            self.__bin(1<<row, self._dim), 
                            self.__bin(1<<col, self._dim ),
                            self.__bin( self._matrix[row][col] , 1)
                            )

                    self._asserts.append( s )

            s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._resMatName, 2 * self._dim, 1 )
            self._declares.append(s)

            for row in range(self._dim):
                for col in range(self._dim):
                    s = 'ASSERT %s[%s@%s]=%s;' %( 
                            self._resMatName, 
                            self.__bin(1<<row, self._dim), 
                            self.__bin(1<<col, self._dim ),
                            self.__bin( self._resMatrix[row][col] , 1)
                            )

                    self._asserts.append( s )

            Matrix.define = True

    def __declare_temp_matrix_invMatrix(self):
        '''
        declare the auxiliary matrix M^\expand'
        '''
        s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._invMatName, 2 * self._dim, 1 )
        self._declares.append(s)

        for i in range(self._dim):
            for j in range(self._dim):
                L = []
                for k in range(self._dim):
                    L.append( '(%s[%s@%s] & %s[%s@%s] & %s & %s)' % (
                        self._matrixName, 
                        self.__bin(1 << i, self._dim),
                        self.__bin(1 << k, self._dim),
                        self._invMatName,
                        self.__bin(1 << k, self._dim),
                        self.__bin(1 << j, self._dim),
                        self._inVec[k], 
                        self._outVec[i], 
                        ) )

                self._asserts.append( 'ASSERT %s = %s[%s@%s] & %s ;' % (
                        self.__xor(L), 
                        self._resMatName, 
                        self.__bin(1<<i, self._dim),
                        self.__bin(1<<j, self._dim),
                        self._outVec[i]
                        ) )

    def __xor(self, xorEles):
        '''
        generate xor constraints
        @ xorEles: a list of strings representing variables or expressions, e.g. [x0, x1, x2]

        @ return : BVXOR(x0, BVXOR(x1, x2) ) for x0 ^ x1 ^ x2
        '''
        s = ''
        assert len(xorEles) > 0
        if len(xorEles) == 1:
            return '%s' %  ( xorEles[0] )
        s += 'BVXOR(%s, %s)' % ( xorEles[0], self.__xor(xorEles[1:]) )
        return s

    def get_declares_asserts(self):
        return self._declares + self._asserts



def main():
    matrix = [ 
    [ 1,1,0,0 ],
    [ 0,1,1,0 ],
    [ 0,1,1,1 ],
    [ 0,1,0,1 ]
    ]
    matrixName = 'MATRIX'
    inv = [0,0,1, 0]
    outv = [0,1,0,0]

    inVec1 = [ 'a%d'%x for x in range(4) ]
    outVec1 = [ 'b%d'%x for x in range(4) ]

    for x in inVec1:
        print ( '%s:BITVECTOR(1);'%x)

    for x in outVec1:
        print ( '%s:BITVECTOR(1);'%x)

    for x in range(4):
        if inv[x]:
            print( 'ASSERT a%d = 0bin1;'%x )
        else:
            print( 'ASSERT a%d = 0bin0;'%x )

    for x in range(4):
        if outv[x]:
            print( 'ASSERT b%d = 0bin1;'%x )
        else:
            print( 'ASSERT b%d = 0bin0;'%x )

    m = Matrix(matrixName, matrix, inVec1, outVec1, 0, 1)
    print ( '\n'.join( m.get_declares_asserts() ) )

    print( 'QUERY FALSE;')
    print( 'COUNTEREXAMPLE;')

if __name__ == '__main__':
    main()

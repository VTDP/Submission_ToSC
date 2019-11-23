class Matrix(object):
    # matrix is 2-fold list, inVec and outVec are both str lists
    def __init__(self, matrixName, matrix,inVec, outVec,  r, p):
        self._matrixName = '%s_%d_%d' % (matrixName, r, p)
        self._matrix = matrix
        self._inVec = inVec
        self._outVec = outVec
        self._dim = len(inVec)
        self._declares = []
        self._asserts = []
        self._matName = 'mat_%s_%d_%d'%(matrixName, r, p)
        self._invMatName = 'inv_mat_%s_%d_%d'%(matrixName, r, p)
        self._resMatName = 'res_mat_%s_%d_%d' % (matrixName, r, p)
        self.__declareMatrix()
        self.__declare_temp_matrix_invMatrix()
        self.__genConstrs()

    def __bin(self, num, length ):
        return '0bin' + bin(num)[2:].zfill(length)

    def __genConstrs(self):
        '''
        TODO: asserts the hamming weights of input vector and that of output vector are equal
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

        '''
        In this function, we check the input vector bit by bit, if the input bit is 1 then we set the 
        res matrix 1 in diagnal
        for the temp matrix, we set the mat & invMat = 1 as MATRIX
        '''
        for row in range(self._dim):
            for col in range(self._dim):
                s = 'ASSERT %s[%s@%s] = IF %s&%s = 0bin1 THEN %s[%s@%s] ELSE 0bin0 ENDIF;'% (
                        self._matName, self.__bin(1<<row, self._dim), self.__bin(1<<col, self._dim),
                        self._outVec[row], 
                        self._inVec[col],
                        self._matrixName, self.__bin(1<<row, self._dim), self.__bin(1<<col, self._dim),
                        )
                self._asserts.append(s)

        for row in range(self._dim):
            s = 'ASSERT %s[%s@%s] = IF %s = 0bin1 THEN 0bin1 ELSE 0bin0 ENDIF;'% (
                        self._resMatName, self.__bin(1<<row, self._dim), self.__bin(1<<row, self._dim),
                        self._outVec[row], 
                        )
            self._asserts.append(s)
        for row in range(self._dim):
            for col in range(self._dim):
                if row != col:
                    s = 'ASSERT  %s[%s@%s] = 0bin0;' % ( self._resMatName, self.__bin( 1 << row, self._dim), self.__bin( 1 << col, self._dim ) )
                    self._asserts.append( s) 

    def __declareMatrix(self):
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

    def __declare_temp_matrix_invMatrix(self):
        s = '%s: ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._matName, 2 * self._dim, 1 )
        self._declares.append(s)

        s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._invMatName, 2 * self._dim, 1 )
        self._declares.append(s)

        s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._resMatName, 2 * self._dim, 1 )
        self._declares.append(s)

        for i in range(self._dim):
            for j in range(self._dim):
                L = []
                for k in range(self._dim):
                    L.append( '(%s[%s@%s] & %s[%s@%s])' % (
                        self._matName, 
                        self.__bin(1 << i, self._dim),
                        self.__bin(1 << k, self._dim),
                        self._invMatName,
                        self.__bin(1 << k, self._dim),
                        self.__bin(1 << j, self._dim)
                        ) )

                self._asserts.append( 'ASSERT %s = %s[%s@%s];' % (
                        self.__xor(L), 
                        self._resMatName, 
                        self.__bin(1<<i, self._dim),
                        self.__bin(1<<j, self._dim)
                        ) )

    def __xor(self, xorEles):
        s = ''
        assert len(xorEles) > 0
        if len(xorEles) == 1:
            return '%s' %  ( xorEles[0] )
        s += 'BVXOR(%s, %s)' % ( xorEles[0], self.__xor(xorEles[1:]) )
        return s

    def get_declares_asserts(self):
#        if not self._asserts or not self._declares:
#            self.__declareMatrix()
#            self.__declare_temp_matrix_invMatrix()
#            self.__genConstrs()
        return self._declares + self._asserts



def main():
    #matrix = [ [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]
    matrix = [ 
    [ 1,1,0,0 ],
    [ 0,1,1,0 ],
    [ 0,1,1,1 ],
    [ 0,1,0,1 ]
    ]
    matrixName = 'MATRIX'
    #inv = [0,0,0,0, 1,1,1,1, 1,1,1,1, 1,1,1,1]
    inv = [1,0,0, 0]
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

class NonSquareMatrix(object):
    # matrix is 2-fold list, inVec and outVec are both str lists
    def __init__(self, matrixName, matrix,inVec, outVec,  r, p):
        self._matrixName = '%s_%d_%d' % (matrixName, r, p)
        self._matrix = matrix
        self._inVec = inVec
        self._outVec = outVec
        self._dimCol = len(inVec)
        self._dimRow = len(outVec)
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
        asserts the hamming weights of input vector and that of output vector are equal
        ''' 
        s = 'ASSERT BVPLUS(%d' % ( self._dimCol + self._dimRow )
        for i in range(self._dimCol):
            s += ', %s@%s' % (self.__bin(0, self._dimCol + self._dimRow - 1 ), self._inVec[i] )
        s += ')'

        s += ' = BVPLUS(%d'% ( self._dimRow + self._dimCol )
            
        for i in range(self._dimRow):
            s += ', %s@%s' % (self.__bin(0, self._dimRow + self._dimCol - 1 ), self._outVec[i] )
        s += ');'
        self._declares.append( s )

        '''
        In this function, we check the input vector bit by bit, if the input bit is 1 then we set the 
        res matrix 1 in diagnal
        for the temp matrix, we set the mat & invMat = 1 as MATRIX
        '''
        for row in range(self._dimRow):
            for col in range(self._dimCol):
                s = 'ASSERT %s[%s@%s] = IF %s&%s = 0bin1 THEN %s[%s@%s] ELSE 0bin0 ENDIF;'% (
                        self._matName, self.__bin(1<<row, self._dimRow), self.__bin(1<<col, self._dimCol),
                        self._outVec[row], 
                        self._inVec[col],
                        self._matrixName, self.__bin(1<<row, self._dimRow), self.__bin(1<<col, self._dimCol),
                        )
                self._asserts.append(s)

        for row in range(self._dimRow):
            s = 'ASSERT %s[%s@%s] = IF %s = 0bin1 THEN 0bin1 ELSE 0bin0 ENDIF;'% (
                        self._resMatName, self.__bin(1<<row, self._dimRow), self.__bin(1<<row, self._dimRow),
                        self._outVec[row], 
                        )
            self._asserts.append(s)

        for row in range(self._dimRow):
            for col in range(self._dimRow):
                if row != col:
                    s = 'ASSERT  %s[%s@%s] = 0bin0;' % ( self._resMatName, self.__bin( 1 << row, self._dimRow), self.__bin( 1 << col, self._dimRow ) )
                    self._asserts.append( s) 

    def __declareMatrix(self):
            s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                    self._matrixName, self._dimRow + self._dimCol, 1 )
            self._declares.append(s)

            for row in range(self._dimRow ):
                for col in range(self._dimCol ):
                    s = 'ASSERT %s[%s@%s]=%s;' %( 
                            self._matrixName, 
                            self.__bin(1<<row, self._dimRow ), 
                            self.__bin(1<<col, self._dimCol ),
                            self.__bin( self._matrix[row][col] , 1)
                            )

                    self._asserts.append( s )

    def __declare_temp_matrix_invMatrix(self):
        s = '%s: ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._matName, self._dimCol + self._dimRow, 1 )
        self._declares.append(s)

        s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._invMatName, self._dimCol + self._dimRow, 1 )
        self._declares.append(s)

        s = '%s : ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' % ( 
                self._resMatName, 2 * self._dimRow, 1 )
        self._declares.append(s)

        for i in range(self._dimRow):
            for j in range(self._dimRow):
                L = []
                for k in range(self._dimCol):
                    L.append( '(%s[%s@%s] & %s[%s@%s])' % (
                        self._matName, 
                        self.__bin(1 << i, self._dimRow),
                        self.__bin(1 << k, self._dimCol),
                        self._invMatName,
                        self.__bin(1 << k, self._dimCol),
                        self.__bin(1 << j, self._dimRow)
                        ) )

                self._asserts.append( 'ASSERT %s = %s[%s@%s];' % (
                        self.__xor(L), 
                        self._resMatName, 
                        self.__bin(1<<i, self._dimRow),
                        self.__bin(1<<j, self._dimRow)
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
    #matrix = [ [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,     0]]
    first = [
[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0] ,
[0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0] ,
[1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0] ,
[1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0] ,
[0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1] ,
[1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0] ,
[1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0] ,
[0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1] ,
[1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0] ,
[0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0] ,
[1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0] ,
[0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0] ,
[1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1] ,
[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1] ,
[0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0] ,
[1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1] ,
[0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0] ,
[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0] ,
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0] ,
[1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0] ,
[0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1] ,
[1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0] ,
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1] ,
[0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1] ,
[0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0] ,
[0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0] ,
[1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0] ,
[0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0] ,
[1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1] ,
[1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1] ,
[0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1] ,
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0] ,
]
    matrixName = 'MATRIX'
    #inv = [0,0,0,0, 1,1,1,1, 1,1,1,1, 1,1,1,1]
    inv = [1 for x in range(24)]
    #outv = [0,0]

    inVec1 = [ 'a%d'%x for x in range(24) ]
    outVec1 = [ 'b%d'%x for x in range(32) ]

    for x in inVec1:
        print ( '%s:BITVECTOR(1);'%x)

    for x in outVec1:
        print ( '%s:BITVECTOR(1);'%x)

    for x in range(24):
        if inv[x]:
            print( 'ASSERT a%d = 0bin1;'%x )
        else:
            print( 'ASSERT a%d = 0bin0;'%x )

    #for x in range(32):
    #    if outv[x]:
    #        print( 'ASSERT b%d = 0bin1;'%x )
    #    else:
    #        print( 'ASSERT b%d = 0bin0;'%x )

    m = NonMatrix(matrixName, first, inVec1, outVec1, 0, 1)
    for i in range(4):
        s = 'ASSERT %s@%s@%s@%s@%s@%s@%s@%s /= 0bin11111111;'% ( 
                outVec1[8 * i + 0], 
                outVec1[8 * i + 1], 
                outVec1[8 * i +2], 
                outVec1[8 * i +3],
                outVec1[8 * i +4], 
                outVec1[8 * i +5],
                outVec1[8 * i +6], 
                outVec1[8 * i +7] )
        m._asserts.append( s )
    print ( '\n'.join( m.get_declares_asserts() ) )

    print( 'QUERY FALSE;')
    print( 'COUNTEREXAMPLE;')

if __name__ == '__main__':
    main()

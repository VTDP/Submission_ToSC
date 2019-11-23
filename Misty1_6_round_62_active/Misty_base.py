from AssertSbox import *
from Matrix import *
import sys

class Misty(object):
    def __init__(self, matNameFL, matrixFL,
                       matNameFO, matrixFO,
                       matNameFI_zero_extended, matrixFI_zero_extended,
                       matNameFI_truncate, matrixFI_truncate,
                       sboxName9, sbox9, sboxDim9, numberOfSbox9,
                       sboxName7, sbox7, sboxDim7, numberOfSbox7,
                       dim,
                       r,
                       inVec, outVec ):

        self._sbox9 = AssertSbox(sboxName9, sbox9, sboxDim9, r, numberOfSbox9)
        self._sbox7 = AssertSbox(sboxName7, sbox7, sboxDim7, r, numberOfSbox7)
        self._sboxDim9 = sboxDim9
        self._sboxDim7 = sboxDim7

        self._matrixNameFL = matNameFL
        self._matrixFL = matrixFL

        self._matrixNameFO = matNameFO
        self._matrixFO = matrixFO
        self._matrixNameFI_zero_extended = matNameFI_zero_extended
        self._matrixFI_zero_extended = matrixFI_zero_extended
        self._matrixNameFI_truncate = matNameFI_truncate
        self._matrixFI_truncate = matrixFI_truncate

        self._dim = dim
        self._round = r
        self._constrs = []
        self._vars = dict()
        self._inVec = inVec
        self._outVec = outVec

        self._constrs += self._sbox9.get_asserts_declares()
        self._constrs += self._sbox7.get_asserts_declares()

    def _declare(self, varName, dim = 1):
        return '%s:BITVECTOR(%d);'%(varName, dim)

    def _addConstr(self, asserts):
        self._constrs.append( asserts )

    def _equal(self, in_var, out_var):
        dim = len(in_var)
        for i in range(dim):
            self._addConstr( 'ASSERT %s= %s;' % (in_var[i], out_var[i]))

    def _declareV(self, varName, round_dim, one_round_dim):
        self._vars[varName] = [ [None for x in range(one_round_dim)] for x in range(round_dim) ]
        for r in range(round_dim):
            for p in range(one_round_dim):
                varx = '%s_%d_%d' % (varName, r, p)
                self._vars[varName][r][p] = varx
                self._addConstr( self._declare( varx ) ) 

    def _Kxor(self, a0, a1, b ):
        s = 'ASSERT '
        s += '~' + a0 +' | ~' + a1 + '= 0bin1;\n'
        s += 'ASSERT '
        s += a0 + ' | ' + a1 + ' | ~' + b + '= 0bin1;\n'
        s += 'ASSERT '
        s += a0 +' | ~' + a1 + ' | ' + b + '= 0bin1;\n'
        s += 'ASSERT '
        s += '~' + a0 + ' | ' + a1 + ' | ' + b + '= 0bin1;'

        return s
    def _Kcopy(self, a, b0, b1 ):
        s = 'ASSERT '
        s += '~' + b0 + ' | ~'+ b1 + ' = 0bin1;\n'
        s += 'ASSERT '
        s += a + ' | ' + b0 + ' | ~' + b1 + ' = 0bin1;\n'
        s += 'ASSERT '
        s += a + ' | ' + '~' +b0 + ' | ' + b1 + ' = 0bin1;\n'
        s += 'ASSERT '
        s += '~' + a + ' | ' + b0 + ' | ' + b1 + ' = 0bin1;'

        return s

    def _block_copy(self, inV, outV1, outV2 ):
        dim = len( inV )
        for i in range(dim):
            self._addConstr( self._Kcopy(inV[i], outV1[i], outV2[i]) )

    def _block_xor(self, inV, outV1, outV2 ):
        dim = len( inV )
        for i in range(dim):
            self._addConstr( self._Kxor(inV[i], outV1[i], outV2[i]) )

    def _declareVariables(self):
        self._declareV( 'MISTY_KX', self._round + 1, self._dim)
        self._declareV( 'MISTY_FL', self._round // 2 + 1, self._dim)
        self._declareV( 'MISTY_FO_IN', self._round, self._dim // 2)
        self._declareV( 'MISTY_FO_OUT', self._round, self._dim // 2)

        self._declareV( 'MISTY_FO_FIRST', self._round, self._dim // 2)
        self._declareV( 'MISTY_FO_SECOND', self._round, self._dim // 2)
        self._declareV( 'MISTY_FO_THIRD', self._round, self._dim // 2)
        self._declareV( 'MISTY_FO_FOURTH', self._round, self._dim // 2)
        self._declareV( 'MISTY_FO_FIFTH', self._round, self._dim // 2)

        varName = 'MISTY_FI_FIRST'
        self._vars[varName] =  [ [ [None for x in range(16)] for x in range(3) ] for x in range(self._round ) ]
        for r in range(self._round):
            for q in range(3):
                for p in range(16):
                    varx = '%s_%d_%d_%d' % (varName, r, q, p)
                    self._vars[varName][r][q][p] = varx
                    self._addConstr( self._declare( varx ) ) 
        varName = 'MISTY_FI_SECOND'
        self._vars[varName] =  [ [ [None for x in range(16)] for x in range(3) ] for x in range(self._round ) ]
        for r in range(self._round):
            for q in range(3):
                for p in range(16):
                    varx = '%s_%d_%d_%d' % (varName, r, q, p)
                    self._vars[varName][r][q][p] = varx
                    self._addConstr( self._declare( varx ) ) 
        varName = 'MISTY_FI_THIRD'
        self._vars[varName] =  [ [ [None for x in range(16)] for x in range(3) ] for x in range(self._round ) ]
        for r in range(self._round):
            for q in range(3):
                for p in range(16):
                    varx = '%s_%d_%d_%d' % (varName, r, q, p)
                    self._vars[varName][r][q][p] = varx
                    self._addConstr( self._declare( varx ) ) 
        varName = 'MISTY_FI_FOURTH'
        self._vars[varName] =  [ [ [None for x in range(16)] for x in range(3) ] for x in range(self._round ) ]
        for r in range(self._round):
            for q in range(3):
                for p in range(16):
                    varx = '%s_%d_%d_%d' % (varName, r, q, p)
                    self._vars[varName][r][q][p] = varx
                    self._addConstr( self._declare( varx ) ) 
        varName = 'MISTY_FI_FIFTH'
        self._vars[varName] =  [ [ [None for x in range(16)] for x in range(3) ] for x in range(self._round ) ]
        for r in range(self._round):
            for q in range(3):
                for p in range(16):
                    varx = '%s_%d_%d_%d' % (varName, r, q, p)
                    self._vars[varName][r][q][p] = varx
                    self._addConstr( self._declare( varx ) ) 

    def _FL(self, in_vars, out_vars, r, p):
        m = Matrix( self._matrixNameFL, self._matrixFL, in_vars, out_vars, r, p)
        self._constrs += m.get_declares_asserts()

    def _FO(self, in_vars, out_vars, r):
        self._FI(in_vars[0:16], self._vars['MISTY_FO_FIRST'][r][0:16], r, 0)
        self._equal( in_vars[16:32], self._vars['MISTY_FO_FIRST'][r][16:32] )

        m = Matrix(self._matrixNameFO, self._matrixFO, self._vars['MISTY_FO_FIRST'][r], self._vars['MISTY_FO_SECOND'][r], r, 0 )
        self._constrs += m.get_declares_asserts()

        self._FI(self._vars['MISTY_FO_SECOND'][r][0:16], self._vars['MISTY_FO_THIRD'][r][0:16],r, 1) 
        self._equal( self._vars['MISTY_FO_SECOND'][r][16:32], self._vars['MISTY_FO_THIRD'][r][16:32] )

        m = Matrix(self._matrixNameFO, self._matrixFO, self._vars['MISTY_FO_THIRD'][r], self._vars['MISTY_FO_FOURTH'][r], r, 1 )
        self._constrs += m.get_declares_asserts()

        self._FI(self._vars['MISTY_FO_FOURTH'][r][0:16], self._vars['MISTY_FO_FIFTH'][r][0:16], r, 2)
        self._equal( self._vars['MISTY_FO_FOURTH'][r][16:32], self._vars['MISTY_FO_FIFTH'][r][16:32] )

        m = Matrix(self._matrixNameFO, self._matrixFO, self._vars['MISTY_FO_FIFTH'][r], self._vars['MISTY_FO_OUT'][r], r, 2 )
        self._constrs += m.get_declares_asserts()

    def _FI(self, in_vars, out_vars, r, p ):
        self._constrs.append( self._sbox9.build_constrs( in_vars[0:9], self._vars['MISTY_FI_FIRST'][r][p][0:9], r, 2 * p ) )
        self._equal( in_vars[9:16], self._vars['MISTY_FI_FIRST'][r][p][9:16] )

        m = Matrix( self._matrixNameFI_zero_extended, self._matrixFI_zero_extended, self._vars['MISTY_FI_FIRST'][r][p], self._vars['MISTY_FI_SECOND'][r][p], r, 2 * p )
        self._constrs += m.get_declares_asserts()

        self._constrs.append( self._sbox7.build_constrs( self._vars['MISTY_FI_SECOND'][r][p][0:7], self._vars['MISTY_FI_THIRD'][r][p][0:7], r,  p  ) )
        self._equal( self._vars['MISTY_FI_SECOND'][r][p][7:16], self._vars['MISTY_FI_THIRD'][r][p][7:16] )

        m = Matrix( self._matrixNameFI_truncate, self._matrixFI_truncate, self._vars['MISTY_FI_THIRD'][r][p], self._vars['MISTY_FI_FOURTH'][r][p], r,  p)
        self._constrs += m.get_declares_asserts()

        self._constrs.append( self._sbox9.build_constrs( self._vars['MISTY_FI_FOURTH'][r][p][0:9], self._vars['MISTY_FI_FIFTH'][r][p][0:9], r, 2 * p + 1 ) )
        self._equal( self._vars['MISTY_FI_FOURTH'][r][p][9:16], self._vars['MISTY_FI_FIFTH'][r][p][9:16] )

        m = Matrix( self._matrixNameFI_zero_extended, self._matrixFI_zero_extended, self._vars['MISTY_FI_FIFTH'][r][p], out_vars, r,2 *  p +1)
        self._constrs += m.get_declares_asserts()


    def _gen_round_constrs(self):
        for r in range(self._round):
            if  r % 2 == 0 and r != 0: 
                self._FL( self._vars['MISTY_KX'][r][0:32], self._vars['MISTY_FL'][r//2][0:32], r, 0 )
                self._FL( self._vars['MISTY_KX'][r][32:64], self._vars['MISTY_FL'][r//2][32:64], r, 1 )


                self._block_copy( self._vars['MISTY_FL'][r//2][0:32], self._vars['MISTY_FO_IN'][r], self._vars['MISTY_KX'][r+1][32:64] )
                self._FO( self._vars['MISTY_FO_IN'][r], self._vars['MISTY_FO_OUT'][r], r )

                self._block_xor( self._vars['MISTY_FO_OUT'][r], self._vars['MISTY_FL'][r//2][32:64], self._vars['MISTY_KX'][r + 1][0:32])
            else:

                self._block_copy( self._vars['MISTY_KX'][r][0:32], self._vars['MISTY_FO_IN'][r], self._vars['MISTY_KX'][r+1][32:64] )
                self._FO( self._vars['MISTY_FO_IN'][r], self._vars['MISTY_FO_OUT'][r], r )

                self._block_xor( self._vars['MISTY_FO_OUT'][r], self._vars['MISTY_KX'][r][32:64], self._vars['MISTY_KX'][r + 1][0:32])

    def _gen_init_constrs(self):
        for i in range(self._dim):
            if i in self._inVec:
                self._addConstr( 'ASSERT %s = 0bin1;' % self._vars['MISTY_KX'][0][i] )
            else:
                self._addConstr( 'ASSERT %s = 0bin0;' % self._vars['MISTY_KX'][0][i] )

        for i in range(32):
            self._addConstr( 'ASSERT %s = 0bin0;' % self._vars['MISTY_KX'][self._round][i] )

        s = 'ASSERT BVPLUS(10,'
        for i in range(32, 63):
            s += '0bin000000000@%s,' % self._vars['MISTY_KX'][self._round][i]
        s += '0bin000000000@%s ) = 0bin0000000001;' % self._vars['MISTY_KX'][self._round][63] 

        self._constrs.append( 'QUERY FALSE;')
        #self._constrs.append( 'COUNTEREXAMPLE;')

    def getConstrs(self):
        self._declareVariables()
        self._gen_round_constrs()
        self._gen_init_constrs()
        
        return self._constrs

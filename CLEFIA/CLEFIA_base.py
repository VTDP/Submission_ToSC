from AssertSbox import *
from Matrix import *
import sys

class CLEFIA( object ):
    def __init__( self,
                  S0_name, S0, S0_dim, S0_num,
                  S1_name, S1, S1_dim, S1_num,
                  M0_name, M0,
                  M1_name, M1,
                  dim, r, inVec, outVec ):

        self._s0 = AssertSbox( S0_name, S0, S0_dim,r,  S0_num )
        self._s1 = AssertSbox( S1_name, S1, S1_dim,r,  S1_num )

        self._s0dim = S0_dim
        self._s1dim = S1_dim

        self._matrixName_M0 = M0_name
        self._matrix_M0 = M0

        self._matrixName_M1 = M1_name
        self._matrix_M1 = M1

        self._dim = dim
        self._round = r 
        self._constrs = []
        self._vars = dict()
        self._inVec = inVec
        self._outVec = outVec

        self._constrs += self._s0.get_asserts_declares()
        self._constrs += self._s1.get_asserts_declares()

    def _declare( self, varName, dim =1 ):
        return '%s:BITVECTOR(%d);' % ( varName, dim )
    def _addConstr( self, asserts ):
        self._constrs.append( asserts )

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

    def _declareVariables( self ):
        self._declareV( 'CLEFIA_X', self._round + 1, self._dim )
        self._declareV( 'CLEFIA_F0_IN', self._round, self._dim // 4)
        self._declareV( 'CLEFIA_F1_IN', self._round, self._dim // 4)
        self._declareV( 'CLEFIA_F0_S_OUT', self._round, self._dim // 4)
        self._declareV( 'CLEFIA_F1_S_OUT', self._round, self._dim // 4)
        self._declareV( 'CLEFIA_F0_OUT', self._round, self._dim // 4)
        self._declareV( 'CLEFIA_F1_OUT', self._round, self._dim // 4)

    def _F0( self, F0_in, sbox_out, F0_out, r ):
        self._constrs.append( self._s0.build_constrs( F0_in[0:8], sbox_out[0:8], r, 0 ) )
        
        self._constrs.append( self._s1.build_constrs( F0_in[8:16], sbox_out[8:16], r, 0 ) )

        self._constrs.append( self._s0.build_constrs( F0_in[16:24], sbox_out[16:24], r, 1 ) )
        
        self._constrs.append( self._s1.build_constrs( F0_in[24:32], sbox_out[24:32], r, 1 ) )

        m = Matrix( self._matrixName_M0, self._matrix_M0, sbox_out, F0_out, r, 0 )
        self._constrs += m.get_declares_asserts()


    def _F1( self, F0_in, sbox_out, F0_out, r ):
        self._constrs.append( self._s1.build_constrs( F0_in[0:8], sbox_out[0:8], r, 2 ) )
        
        self._constrs.append( self._s0.build_constrs( F0_in[8:16], sbox_out[8:16], r, 2 ) )

        self._constrs.append( self._s1.build_constrs( F0_in[16:24], sbox_out[16:24], r, 3 ) )
        
        self._constrs.append( self._s0.build_constrs( F0_in[24:32], sbox_out[24:32], r, 3 ) )

        m = Matrix( self._matrixName_M1, self._matrix_M1, sbox_out, F0_out, r, 0 )
        self._constrs += m.get_declares_asserts()

    def _gen_round_constrs( self ):
        for r in range(self._round ):
            self._block_copy( self._vars['CLEFIA_X'][r][0:32], self._vars['CLEFIA_F0_IN'][r], self._vars['CLEFIA_X'][r+1][96:128] )
            self._F0( self._vars['CLEFIA_F0_IN'][r], self._vars['CLEFIA_F0_S_OUT'][r], self._vars['CLEFIA_F0_OUT'][r], r )       
            self._block_xor( self._vars['CLEFIA_F0_OUT'][r], self._vars['CLEFIA_X'][r][32:64], self._vars['CLEFIA_X'][r+1][0:32] )

            self._block_copy( self._vars['CLEFIA_X'][r][64:96], self._vars['CLEFIA_F1_IN'][r], self._vars['CLEFIA_X'][r+1][32:64] )
            self._F1( self._vars['CLEFIA_F1_IN'][r], self._vars['CLEFIA_F1_S_OUT'][r], self._vars['CLEFIA_F1_OUT'][r], r )       
            self._block_xor( self._vars['CLEFIA_F1_OUT'][r], self._vars['CLEFIA_X'][r][96:128], self._vars['CLEFIA_X'][r+1][64:96] )

    def _gen_init_constrs(self):
        for i in range(self._dim):
            if i in self._inVec:
                self._addConstr( 'ASSERT %s = 0bin1;' % self._vars['CLEFIA_X'][0][i] )
            else:
                self._addConstr( 'ASSERT %s = 0bin0;' % self._vars['CLEFIA_X'][0][i] )

        for i in [x for x in range(32)] + [x for x in range(64, 96)]:
            self._addConstr( 'ASSERT %s = 0bin0;' % self._vars['CLEFIA_X'][self._round][i] )

        s = 'ASSERT BVPLUS(10,'
        for i in [x for x in range(32, 64)] + [x for x in range(96, 127)]:
            s += '0bin000000000@%s,' % self._vars['CLEFIA_X'][self._round][i]
        s += '0bin000000000@%s ) = 0bin0000000001;' % self._vars['CLEFIA_X'][self._round][127] 

        self._constrs.append( 'QUERY FALSE;')
        #self._constrs.append( 'COUNTEREXAMPLE;')

    def getConstrs(self):
        self._declareVariables()
        self._gen_round_constrs()
        self._gen_init_constrs()
        
        return self._constrs

        


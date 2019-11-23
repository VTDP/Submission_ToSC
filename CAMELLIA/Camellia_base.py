from AssertSbox import *
from Matrix import *
import sys


def rot_left( X, low, high ):
    Y = []
    for x in X:
        Y.append( x )
    for i in range(8):
        X[low + i] = ( Y[ (low + ( i + 1 ) % 8 ) ] )

def rot_right( X, low, high ):
    Y = []
    for x in X:
        Y.append( x )
    for i in range(8):
        X[low + i] = ( Y[ (low + ( i - 1 + 8 ) % 8 ) ] )

class Camellia( object ):
    def __init__( self, matNameP, matrixP, matNameP_inv, matrixP_inv,
            matNameFL, matrixFL, matNameFL_inv, matrixFL_inv,
            sboxName, sbox, sboxDim, numberOfSbox, 
            dim, r, mid_r, inVec, outVec ):

        self._sbox = AssertSbox( sboxName, sbox, sboxDim, r, numberOfSbox )
    
        self._matNameFL = matNameFL
        self._matrixFL = matrixFL
        self._matNameFL_inv = matNameFL_inv
        self._matrixFL_inv = matrixFL_inv
        self._matNameP = matNameP
        self._matrixP = matrixP

        self._matNameP_inv = matNameP_inv
        self._matrixP_inv = matrixP_inv

        self._dim = dim
        self._round = r
        self._midRound = mid_r
        self._constrs = []
        self._vars = dict()
        self._inVec = inVec 
        self._outVec = outVec 

        self._constrs += self._sbox.get_asserts_declares()


    def _declare(self, varName, dim = 1):
        return '%s:BITVECTOR(%d);'%(varName, dim)

    def _addConstr(self, asserts):
        self._constrs.append( asserts )

    def _declareV(self, varName, round_dim, one_round_dim):
        if round_dim > 0:
            self._vars[varName] = [ [None for x in range(one_round_dim)] for x in range(round_dim) ]
            for r in range(round_dim):
                for p in range(one_round_dim):
                    varx = '%s_%d_%d' % (varName, r, p)
                    self._vars[varName][r][p] = varx
                    self._addConstr( self._declare( varx ) ) 
        else:
            self._vars[varName] = [ None for x in range(one_round_dim)]
            for p in range(one_round_dim):
                varx = '%s_%d' % ( varName,  p )
                self._vars[varName][p] = varx
                self._addConstr( self._declare(varx) )

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
        self._declareV( 'Camellia_KX', self._round + 1, self._dim )
        self._declareV( 'Camellia_inSbox', self._round, self._dim // 2)
        self._declareV( 'Camellia_inP', self._round, self._dim // 2)
        self._declareV( 'Camellia_outP', self._round, self._dim // 2)
        self._declareV( 'Camellia_inFL', 0, self._dim )

    def _sboxLayer( self, in_sbox, out_sbox, r ):
        rot_left( in_sbox, 24, 32 ) 
        rot_left( in_sbox, 48, 56 )
        self._constrs.append( self._sbox.build_constrs( in_sbox[0:8],   out_sbox[0:8],   r, 0 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[8:16],  out_sbox[8:16],  r, 1 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[16:24], out_sbox[16:24], r, 2 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[24:32], out_sbox[24:32], r, 3 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[32:40], out_sbox[32:40], r, 4 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[40:48], out_sbox[40:48], r, 5 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[48:56], out_sbox[48:56], r, 6 ) )
        self._constrs.append( self._sbox.build_constrs( in_sbox[56:64], out_sbox[56:64], r, 7 ) )

        rot_right( out_sbox, 16, 24 )
        rot_right( out_sbox, 40, 48 )

        rot_left( out_sbox, 8, 16 )
        rot_left( out_sbox, 32, 40 )

    def _FL( self, in_FL, out_FL ):
        m = Matrix( self._matNameFL, self._matrixFL, in_FL[0:64], out_FL[0:64], 0, 0)
        self._constrs += m.get_declares_asserts()

        m = Matrix( self._matNameFL_inv, self._matrixFL_inv, in_FL[64:128], out_FL[64:128], 0, 0)
        self._constrs += m.get_declares_asserts()

    def _P ( self, in_P, out_P, r ):
        m = Matrix( self._matNameP, self._matrixP, in_P, out_P, r, 0) 
        self._constrs += m.get_declares_asserts()       

    def _gen_round_constrs ( self ):
        for r in range( self._round ):
            if r == self._midRound - 1: 
                self._block_copy( self._vars['Camellia_KX'][r][0:64], self._vars['Camellia_inSbox'][r], self._vars['Camellia_inFL'][64:128] )
                self._sboxLayer( self._vars['Camellia_inSbox'][r], self._vars['Camellia_inP'][r], r )
                self._P( self._vars['Camellia_inP'][r], self._vars['Camellia_outP'][r], r )
                self._block_xor( self._vars['Camellia_KX'][r][64:128], self._vars['Camellia_outP'][r], self._vars['Camellia_inFL'][0:64])
                self._FL( self._vars['Camellia_inFL'], self._vars['Camellia_KX'][r+1] )
            else:
                self._block_copy( self._vars['Camellia_KX'][r][0:64], self._vars['Camellia_inSbox'][r], self._vars['Camellia_KX'][r+1][64:128] )
                self._sboxLayer( self._vars['Camellia_inSbox'][r], self._vars['Camellia_inP'][r], r )
                self._P( self._vars['Camellia_inP'][r], self._vars['Camellia_outP'][r], r )
                self._block_xor( self._vars['Camellia_KX'][r][64:128], self._vars['Camellia_outP'][r], self._vars['Camellia_KX'][r+1][0:64])

    def _gen_init_constrs(self):
        '''
        add the initial and stopping rules
        '''
        for i in range(self._dim):
            if i in self._inVec:
                self._addConstr( 'ASSERT %s = 0bin1;' % self._vars['Camellia_KX'][0][i] )
            else:
                self._addConstr( 'ASSERT %s = 0bin0;' % self._vars['Camellia_KX'][0][i] )

        # C_0 + ... + C_6 + C_32 + ... + C_63 = 1
        s = 'ASSERT BVPLUS(10, 0bin000000000@%s ' % self._vars['Camellia_KX'][self._round][64]
        for i in range(65, 128):
            s += ', 0bin000000000@%s' % self._vars['Camellia_KX'][self._round][i]  
        s += ') = 0bin0000000001;'
        self._constrs.append( s ) 
        self._constrs.append( 'QUERY FALSE;')


    def getConstrs(self):
        self._declareVariables()
        self._gen_round_constrs()
        self._gen_init_constrs()
        
        return self._constrs

        

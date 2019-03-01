class GenMatrix(object):
    def __init__(self, func, dim):
        self._func = func
        self._dim = dim
        self._matrix = [ [ None for x in range(self._dim) ] for x in range(self._dim) ]
        self._genMatrix()

    def _genMatrix(self):
        for i in range(self._dim):
            res = self._int_2_bit( self._func(1 << ( self._dim - i - 1) ) )
            for j in range(self._dim):
                self._matrix[j][i] = res[j]

    def _bit_2_int(self, bits):
        assert len(bits) == self._dim
        res = 0
        for i in range(len(bits)):
            res ^= bits[i] << (self._dim - 1 - i)
        return res

    def _int_2_bit(self, num):
        bits = [0 for x in range(self._dim)]
        for i in range(len(bits)):
            bits[i] = num >> (self._dim - 1 - i) & 1
        return bits

    def getMatrix (self):
        return self._matrix

def rol( x ):
    return ( x << 1 ) | ( x >> 15)

# FL function
def FL(num):
    l = num >> 16 & 0xffff
    r = num & 0xffff

    res_r = ( rol(l) ^ r )  
    res_l = rol( res_r) ^ l
    return ( res_l << 16 ) | res_r 

def FO(num):
    l = num >> 16 & 0xffff
    r = num & 0xffff
    res_l = r
    res_r = l ^ r
    return ( res_l << 16 ) | res_r

def FI_extend(num):
    l = num >> 7 & 0x1ff
    r = num & 0x7f
    res_l = r
    res_r = l ^ r
    return (res_l << 9) | res_r

def FI_truncate(num):
    l = num >> 9 & 0x7f
    r = num & 0x1ff
    res_l = r
    res_r = ( l ^ r ) & 0x7f
    return (res_l << 7) | res_r

def FI_last ( num ):
    l = num >> 9 & 0x7f
    r = num & 0x1ff

    new_l = l ^ r
    new_r = r

    return ( new_l << 9 ) | ( new_r )

def xtime( x ):
    if x >> 7 & 0x1:
        return ((x << 1) ^ 0x1d) & 0xff
    else:
        return x << 1 & 0xff

def mul( x, y ):
    base = [x]
    for i in range(1, 8):
        x = xtime(x)
        base.append( x )
    res = 0
    for i in range( 8 ):
        res ^=  ( y >> i & 0x1 ) * base[i] 

    return res

def feildMul( x ):
    x0 = x >> 24 & 0xff
    x1 = x >> 16 & 0xff
    x2 = x >> 8 & 0xff
    x3 = x >> 0 & 0xff

    y0 = mul( 1, x0 ) ^ mul(8, x1) ^ mul( 2, x2 ) ^ mul( 0xa, x3 )
    y1 = mul( 8, x0 ) ^ mul(1, x1) ^ mul( 0xa, x2 ) ^ mul( 2, x3 )
    y2 = mul( 2, x0 ) ^ mul(0xa, x1) ^ mul( 1, x2 ) ^ mul( 0x8, x3 )
    y3 = mul( 0xa, x0 ) ^ mul(0x2, x1) ^ mul( 0x8, x2 ) ^ mul( 0x1, x3 )

    return (y0 << 24) | (y1 << 16) | (y2 << 8) | y3  



block = 32
def main():
    m = GenMatrix(feildMul, block)
    mat = m.getMatrix() 
    print ('[')
    for i in range(block):
        print ( mat[i], ',' )
    print ( ']' )

if __name__ == '__main__':
    main()



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

# FL function
def FL(num):
    l = num >> 16 & 0xffff
    r = num & 0xffff

    res_r = r ^ l
    res_l = res_r ^ l
    return ( res_l << 16 ) | res_r 

def FL_1(num):
    l = num >> 16 & 0xffff
    r = num & 0xffff

    res_r = r 
    res_l = res_r ^ l
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

block = 32
def main():
    m = GenMatrix(FL_1, block)
    mat = m.getMatrix() 
    print ('[')
    for i in range(block):
        print ( mat[i], ',' )
    print ( ']' )

if __name__ == '__main__':
    main()



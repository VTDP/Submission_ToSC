#include<iostream>
#include<random>
#include<cstring>

using namespace std;

typedef unsigned char Cell;

const int R = 6;

Cell sbox[16] = {0xc, 0x6, 0x9, 0x0, 0x1, 0xa, 0x2, 0xb, 0x3, 0x8, 0x5, 0xd, 0x4, 0xe, 0x7, 0xf};

void SB( Cell x[4][4] )
{
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            x[i][j] = sbox[ x[i][j] ];
}

void ATK( Cell x[4][4], Cell Key[4][4] )
{
    random_device rd;
    for (int i = 0; i < 2; i++ )
        for ( int j = 0; j < 4; j++ )
            x[i][j] ^= Key[i][j];
}

void MC( Cell x[4][4] )
{
    Cell tmp[4][4];
    memcpy( tmp, x, 16 );
    for (int col = 0; col < 4; col++ )
    {
        x[0][col] = tmp[0][col] ^ tmp[2][col] ^ tmp[3][col];
        x[1][col] = tmp[0][col];
        x[2][col] = tmp[1][col] ^ tmp[2][col];
        x[3][col] = tmp[0][col] ^ tmp[2][col];
    }
}

void SR( Cell x[4][4] )
{
    Cell tmp[4][4];
    memcpy(tmp, x, 16);

    x[0][0] = tmp[0][0];
    x[0][1] = tmp[0][1];
    x[0][2] = tmp[0][2];
    x[0][3] = tmp[0][3];
    
    x[1][0] = tmp[1][3];
    x[1][1] = tmp[1][0];
    x[1][2] = tmp[1][1];
    x[1][3] = tmp[1][2];

    x[2][0] = tmp[2][2];
    x[2][1] = tmp[2][3];
    x[2][2] = tmp[2][0];
    x[2][3] = tmp[2][1];

    x[3][0] = tmp[3][1];
    x[3][1] = tmp[3][2];
    x[3][2] = tmp[3][3];
    x[3][3] = tmp[3][0];
}

void encrypt( Cell x[4][4], Cell RK[R][4][4], int round )
{
    for (int i = 0; i < R; i++ )
    { SB(x); ATK(x, RK[i]);SR(x); MC(x); }
}


int main()
{
    random_device rd;
    
    Cell res0[4][4] = { 0 };
    Cell res1[4][4] = { 0xf, 0xf, 0xf, 0xf, 
                        0xf, 0xf, 0xf, 0xf,
                        0xf, 0xf, 0xf, 0xf, 
                        0xf, 0xf, 0xf, 0xf  };

    for ( int test = 0; test < 100; test++ )
    {
    Cell RK[R][4][4] = { 0};
    for (int i = 0; i < R; i++ )
        for ( int j = 0; j < 4; j++ )
            for ( int k = 0; k < 4; k++ )
                RK[i][j][k] = rd() % 16;

    Cell x[4][4] = { 0};
    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            x[i][j] = rd() % 16;
    
    Cell sum[4][4] = {0};
    for(int x00 = 0; x00 < 16; x00++ )
    for(int x11 = 0; x11 < 16; x11++ )
    for(int x22 = 0; x22 < 16; x22++ )
    for(int x33 = 0; x33 < 16; x33++ )
    {
        Cell tmp[4][4] = {0};
        memcpy(tmp, x, 16);
        tmp[0][0] = Cell(x00);
        tmp[1][1] = Cell(x11);
        tmp[2][2] = Cell(x22);
        tmp[3][3] = Cell(x33);

        encrypt(tmp,RK, R);

    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            sum[i][j] ^= tmp[i][j];
    }

    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            res0[i][j] |= sum[i][j];
    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            res1[i][j] &= sum[i][j];
   // cout << "TEST " << test << endl;
   // for ( int i = 0; i < 4; i++ )
   //     for ( int j = 0; j < 4; j++ )
   //         cout << hex << int(res[i][j]) << ' ';
   // cout << endl;
    }
    cout << '0' << endl;
    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            cout << hex << int(res0[i][j]) << ' ';
    cout << endl;
    cout << '1' << endl;
    for ( int i = 0; i < 4; i++ )
        for ( int j = 0; j < 4; j++ )
            cout << hex << int(res1[i][j]) << ' ';
    cout << endl;
}

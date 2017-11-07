#!/usr/bin/env python3

import random
import sys
import numpy as np
import argparse

def factory(n):
     s = 0
     m = 0
     odd = n & 1
     # n should be an even number
     while odd == 0:
         s = s + 1
         n = n >> 1 # n = n / 2
         # odd or even checking
         # for example n = 5 then its binary form is 101
         # 5 & 1 = 101 & 001 = 001
         # if n = 6 then its binary form is 110
         # 110 & 001 = 6 & 1 = 000
         odd = n & 1
     m = n

# m should be an odd number now
     return s, m

def powMod(a, m, n):
     # trival case
     if m == 1:
         return a
     # a kind of russian peasant algorithm on exponent
     odd = m & 1
     # even case
     if odd == 0:
         tmp = (a**2) % n
         tm = int(m / 2)
         return powMod(tmp, tm, n)
     # odd case
     return (a * powMod(a , m - 1, n)) % n

def miler_rabin(n):
     # trival case
     if  n < 1:
         return False
     if  n < 4:
         return True

     # Given n, find s so that n-1=2sq for some odd q.
     s, m = factory(n - 1)

     # n is even when s = 0
     if s < 1:
         return False

     # get a random number in range 0 to n
     # Pick a random a ? {1, ..., n-1}
     a = random.randrange(2, n - 1)


     # If aq=1 then n passes (and exit).
     b =  powMod(a, m ,n) #pow(a, m)


     if b % n == 1:
         return True

     # For i=0,...,s-1 see if a2iq=-1. If so, n passes (and exit).
     for k in range(0, s):
         # b = -1 (mod n)
         # then b + 1 = 0 (mod n)
         b_ = b + 1
         if b_ % n == 0 :
             return True
         b = powMod(b,2,n)# b = pow(b, 2) % n

     return False


def get_prime(key_length):
    n = random.getrandbits(key_length)

    while miler_rabin(n) == False:
        n = random.getrandbits(key_length)
    return n

def gcd(a,b):
    while b != 0:
        a , b = b, a % b
    print(a)
    return a

def multiInverse(e, phi):

    x = 0
    x1 = 1
    y = 1
    y1 = 0
    phi2 = phi
    while phi2 != 0:
        q, r = (e // phi2, e % phi2)
        e, phi2 = phi2, r
        x, x1 = x1 - q * x, x
        y, y1 = y1 - q * y, y

    if x1 < 0:
        #print(phi + x1)
        return phi + x1
    #print(x1)
    return x1


def rsaKeyGen(b):

    p = get_prime(b/2)
    q = get_prime(b/2)

    while p == q:
        q = get_prime(b/2)

    n = p * q
    phi = (p -1) * (q - 1)

    e = 17

    d = multiInverse(e, phi)

    return(n, e, d)

def rsaEncrypt(m, e, n):
    return powMod(m, e, n)

def rsaDecrypt(c, d, n):
    return powMod(c, d, n)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('func')
    parser.add_argument('-k', nargs ='?')
    parser.add_argument('-i', nargs ='?')
    parser.add_argument('-o', nargs ='?')
    parser.add_argument('-p', nargs ='?')
    parser.add_argument('-s', nargs ='?')
    parser.add_argument('-n', nargs ='?')

    args = parser.parse_args()

    func = args.func



    if func == "rsa-enc":
        if args.k != None:
            kF = open(args.k, 'r')
            lines = kF.readlines()
            kF.close()
            bits = int(lines[0])
            n = int(lines[1])
            e = int(lines[2])

        if args.i != None:
            iF = open(args.i, 'r')
            m = int(iF.readline())
            iF.close()

        if args.o != None:
            oF = open(args.o, 'wb')

        oF.write(str(rsaEncrypt(m, e, n)) + '\n')
        oF.close()
        return


    if func == "rsa-dec":
        if args.k != None:
            kF = open(args.k, 'r')
            lines = kF.readlines()
            kF.close()
            bits = int(lines[0])
            n = int(lines[1])
            d = int(lines[2])

        if args.i != None:
            iF = open(args.i, 'r')
            c = int(iF.readline())
            iF.close()

        if args.o != None:
            oF = open(args.o, 'wb')

        oF.write(str(rsaDecrypt(c, d, n)) + '\n')
        oF.close()
        return

    if func == "rsa-keygen":
        if args.p != None:
            pF = open(args.p, 'wb')

        if args.s != None:
            sF = open(args.s, 'wb')

        if args.n != None:
            bits = int(args.n)

        n, e, d = rsaKeyGen(bits)

        pF.write(str(bits) + '\n')
        pF.write(str(n) + '\n')
        pF.write(str(e) + '\n')
        pF.close()

        sF.write(str(bits) + '\n')
        sF.write(str(n) + '\n')
        sF.write(str(d) + '\n')
        sF.close()



if __name__ == '__main__':
	main()





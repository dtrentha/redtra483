#!/usr/bin/env python3


def rsaKeyGen(b): 
	
	p = get_prime(b/2)
	q = get prime(b/2)

	while p == q:
		q = get_prime(b/2)
	
	pq = p * q
	phi = (p -1) * (q - 1)
	
	

	return(pq, e, d)
	

def modExp(base, exp, mod):
    if mod == 1:
		return 0
	c = 1
	while exp > 0:
		if exp%2 == 1:
			c = (base*c) % mod;
		base = (base*base) % mod;
		exp //= 2
	return c

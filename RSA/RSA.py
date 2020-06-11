from random import randint
from Miller_Rabin import *

def gen_large_prime(key_size):
    i = 0
    while i < 1000:
        n = randint(2**(key_size - 1), 2**key_size)
        if MR(n, 20):
            return n
        i += 1
    return 0


def gcd(a, b):
    while b != 0:
        a, b = b, a%b
    return a


def mult_inverse(a, b): #TODO
    x, y, x0, y0, a0, b0 = 0, 1, 1, 0, a, b
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, x0) = ((x0 - (q * x)), x)
        (y, y0) = ((y0 - (q * y)), y)
    if x0 < 0:
        x0 += b0
    if y0 < 0:
        y0 += a0
    return x0


def Keygen(key_size):
    p = gen_large_prime(key_size)
    q = gen_large_prime(key_size)
    while p == q:
        q = gen_large_prime(key_size)
    print("p = ", p)
    print("q = ", q)
    assert p != 0 or q != 0

    n = p*q
    phi = (p - 1)*(q - 1)  # totient of n
    e = randint(1, phi)
    g = gcd(e, phi)

    while g != 1:
        e = randint(1, phi)
        g = gcd(e, phi)

    d = mult_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(public_key, plaintext):
    key, n = public_key
    ciphertext = [bin_pow(ord(i), key, n) for i in plaintext]
    return ciphertext


def decrypt(private_key, ciphertext):
    key, n = private_key
    plaintext = [chr(bin_pow(i, key, n)) for i in ciphertext]
    return plaintext


if __name__ == "__main__":
    pt = input()
    public, private = Keygen(20)
    ct = encrypt(public, pt)
    print(ct)
    print(decrypt(private, ct))
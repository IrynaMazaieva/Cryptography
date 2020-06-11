from consts import *
from functions import *

from hashlib import sha256

len_word = 32 // 8
len_block = 512 // 8

text = input()
text = bytes(text, encoding='utf-8')
text = padd(text)
text = split_text(text)

hashes = []
for i in range(len(H)):
    H[i] = int(str(H[i]), 16)

for j in range(len(text)):
    w = text[j]
    for i in range(16, 64):
        s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ shr(w[i - 15], 3)
        s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ shr(w[i - 2], 10)
        w.append(bitssum(w[i - 16], s0, w[i - 7], s1))

    a, b, c, d, e, f, g, h = H

    for i in range(64):
        t2 = bitssum(S0(a), Ma(a, b, c))
        t1 = bitssum(h, S1(e), Ch(e, f, g), int(str(K[i]), 16), w[i])
        h, g, f, e, d, c, b, a = g, f, e, bitssum(d, t1), c, b, a, bitssum(t1, t2)
    has = bitssum(a, b, c, d, e, f, g, h, H)

    hashes.append(has)
    has = 0

Hash = bitssum(hashes)
print(hex(Hash))


data = input('Enter plaintext data: ')
output = sha256(data.encode('utf-8'))

print(output.hexdigest())

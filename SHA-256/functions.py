def rotr(x, n):
    assert 0 <= n <= x.bit_length()
    return (x << n) | (x >> x.bit_length() - n)


def rotl(x, n):
    assert 0 <= n < x.bit_length()
    return (x >> n) | (x << x.bit_length() - n)


def shr(x, n):
    return x >> n


def S0(a):
    return rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)


def Ma(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def S1(e):
    return rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)


def Ch(e, f, g):
    return (e & f) ^ ((~e) & g)


def padd(word):
    l = len(word) * 8  # because 1 symbol equal 1 byte; 1 byte == 8 bits
    k = (448 - l - 1) % 512
    pad = hex(int('1' + k * '0'))[2:]
    return word + bytes.fromhex(pad) + l.to_bytes(2, byteorder='big')


def split_text(text):
    len_word = 32 // 8
    len_block = 512 // 8
    words = []
    block = []
    for i in range(len(text) // len_word):
        b = text[i * len_word : (i + 1) * len_word].hex()
        block.append(int(b, 16))
        if i != 0 and (i + 1) % (len_block//len_word) == 0:
            words.append(block)
            block = []
    return words


def bitssum(*args):
    s = 0
    for i in args:
        if type(i) is list:
            for j in range(len(i)):
                s += i[j]
        else:
            s += i

    return s


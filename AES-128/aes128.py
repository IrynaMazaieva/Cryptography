from const import *
import random
# Function of multiplication in Galua space:


def mul_02(a):
    if a < 0x80:
        return (a << 1) % 0x100
    else:
        return ((a << 1) ^ 0x1b) % 0x100


def mul_03(a):
    return mul_02(a) ^ a


def mul_09(a):
    return mul_02(mul_02(mul_02(a))) ^ a


def mul_0b(a):
    return mul_02(mul_02(mul_02(a))) ^ mul_02(a) ^ a


def mul_0d(a):
    return mul_02(mul_02(mul_02(a))) ^ mul_02(mul_02(a)) ^ a


def mul_0e(a):
    return mul_02(mul_02(mul_02(a))) ^ mul_02(mul_02(a)) ^ mul_02(a)


# The individual transformations:

def SubBytes(state, inv=False):
    if not inv:
        box = sbox
    else:
        box = inv_sbox

    for i in range(len(state)):
        for j in range(len(state[i])):
            x = state[i][j] // 0x10
            y = state[i][j] % 0x10
            state[i][j] = box[16*x + y]  # because our S-box not a matrix
    return state


def ShiftRows(state, inv=False):
    def left(massive, i):
        res = massive[:]
        for j in range(i):
            temp = res[1:]
            temp.append(res[0])
            res[:] = temp[:]
        return res

    def right(massive, i):
        res = massive[:]
        for j in range(i):
            tmp = res[:-1]
            tmp.insert(0, res[-1])
            res[:] = tmp[:]
        return res

    if not inv:
        for i in range(1, nb):
            state[i] = left(state[i], i)
    else:
        for i in range(1, nb):
            state[i] = right(state[i], i)
    return state


def MixColumns(state, inv=False):
    for i in range(nb):
        if not inv:
            s0 = mul_02(state[0][i]) ^ mul_03(state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ mul_02(state[1][i]) ^ mul_03(state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ mul_02(state[2][i]) ^ mul_03(state[3][i])
            s3 = mul_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ mul_02(state[3][i])
        else:
            s0 = mul_0e(state[0][i]) ^ mul_0b(state[1][i]) ^ mul_0d(state[2][i]) ^ mul_09(state[3][i])
            s1 = mul_09(state[0][i]) ^ mul_0e(state[1][i]) ^ mul_0b(state[2][i]) ^ mul_0d(state[3][i])
            s2 = mul_0d(state[0][i]) ^ mul_09(state[1][i]) ^ mul_0e(state[2][i]) ^ mul_0b(state[3][i])
            s3 = mul_0b(state[0][i]) ^ mul_0d(state[1][i]) ^ mul_09(state[2][i]) ^ mul_0e(state[3][i])
        state[0][i], state[1][i], state[2][i], state[3][i] = s0, s1, s2, s3
    return state


def AddRoundKey(state, key, rounda=0):
    for i in range(nk):
        state[0][i] = state[0][i] ^ key[0][nb * rounda + i]
        state[1][i] = state[1][i] ^ key[1][nb * rounda + i]
        state[2][i] = state[2][i] ^ key[2][nb * rounda + i]
        state[3][i] = state[3][i] ^ key[3][nb * rounda + i]
    return state


def KeyExpansion(key):
    key_s = []
    for i in key:
        key_s.append(ord(i))

    if len(key_s) < 4 * nk:
        for i in range(4 * nk - len(key_s)):
            key_s.append(0x01)

    key_schedule = [[], [], [], []]
    for i in range(4):
        for j in range(nk):
            key_schedule[i].append(key_s[i + 4*j])

    for i in range(nk, nb * (nr + 1)):  # 'i' - number of columns, 'j' - number of rows
        if i % nk == 0:
            temporary_key = []
            for j in range(1, 4):
                temporary_key.append(key_schedule[j][i - 1])
            temporary_key.append(key_schedule[0][i - 1])

            for j in range(len(temporary_key)):
                temporary_key[j] = sbox[16 * (temporary_key[j] // 0x10) + (temporary_key[j] % 0x10)]

            for j in range(4):
                key_schedule[j].append((key_schedule[j][i - 4]) ^ (temporary_key[j]) ^ (rcon[j][int(i / nk - 1)]))

        else:
            for j in range(4):
                key_schedule[j].append(key_schedule[j][i - 4] ^ key_schedule[j][i - 1])
    return key_schedule

# Cipher


def encrypt(plain_text, key):
    state = [[], [], [], []]
    for i in range(4):
        for j in range(nb):
            state[i].append(int(plain_text[i + 4 * j]))
    key_schedule = KeyExpansion(key)
    state = AddRoundKey(state, key_schedule)

    for rounda in range(1, nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, key_schedule, rounda) # 'rounda' because 'round' is built-in name =)

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, key_schedule, nr)

    cipher_text = [None for i in range(4 * nb)]
    for i in range(4):
        for j in range(nb):
            cipher_text[i + 4*j] = state[i][j]
    return cipher_text


def decrypt(cipher_text, key):
    state = [[], [], [], []]
    for i in range(4):
        for j in range(nb):
            state[i].append(cipher_text[i + 4 * j])
    key_schedule = KeyExpansion(key)
    state = AddRoundKey(state, key_schedule, nr)

    for rounda in range(nr - 1, 0, -1):
        state = ShiftRows(state, inv=True)
        state = SubBytes(state, inv=True)
        state = AddRoundKey(state, key_schedule, rounda)  # 'rounda' because 'round' is built-in name =)
        state = MixColumns(state, inv=True)

    state = ShiftRows(state, inv=True)
    state = SubBytes(state, inv=True)
    state = AddRoundKey(state, key_schedule)

    plain_text = [None for i in range(4 * nb)]
    for i in range(4):
        for j in range(nb):
            plain_text[i + 4 * j] = state[i][j]
    return plain_text


if __name__ == "__main__":
    #1
    k = '7564906748398462'
    print('Used key: ', k)
    pl = '1254863450548632'
    print("Plain text: ", pl)
    ct = encrypt(pl, k)
    print('Cipher text: ', ct)
    pt = decrypt(ct, k)
    print("Decrypted text: ", pt)

    #2 one bit changed
    pl = '2254863450548632'
    print("\nPlain text: ", pl)
    ct = encrypt(pl, k)
    print('Cipher text: ', ct) # ciphertext changes almost every bit
    pt = decrypt(ct, k)
    print("Decrypted text: ", pt)

from aes128 import encrypt, decrypt
from random import randint



def cbc(process, text, key):

    def cbc_encrypt(plaintext, key):
        blocks = []
        iv = [randint(0, 9) for i in range(16)]
        ciphertext = [iv]
        i = 0
        for k in range(len(plaintext)//16):
            bl = []
            while len(bl) != 16:
                bl.append(int(plaintext[i]))
                i += 1
            blocks.append(bl)
        previous = iv
        for block in blocks:
            block = [(i ^ j) for (i, j) in zip(block, previous)]
            block = encrypt(block, key)
            previous = block
            ciphertext.append(block)
        ct = ''
        for i in range(len(ciphertext) - 1, -1, -1):
            for j in range(len(ciphertext[i])):
                ct += str(ciphertext[i][j])
        print('Cipher text: ', ct)
        return ciphertext

    def cbc_decrypt(ciphertext, key):
        blocks = ciphertext
        plaintext = []
        for i in range(len(blocks) - 1, -1, -1):
            block = decrypt(blocks[i], key)
            block = [(i ^ j) for (i, j) in zip(blocks[i - 1], block)]
            plaintext.append(block)
        pl = ''
        for i in range(len(plaintext) - 2, -1, -1):
            for j in range(len(plaintext[i])):
                pl += str(plaintext[i][j])
        return pl

    if process == 'encrypt':
        text = cbc_encrypt(text, key)
    else:
        text = cbc_decrypt(text, key)
    return text

def ctr(process, text, key):
    def ctr_encrypt(plaintext, key):
        ctr = ''
        for i in range(16):
             ctr += str(randint(1, 9))
        ctr = int(ctr)

        blocks = []
        i = 0
        for k in range(len(plaintext)//16):
            bl = []
            while len(bl) != 16:
                bl.append(int(plaintext[i]))
                i += 1
            blocks.append(bl)

        ciphertext = [ctr]

        for i in range(len(blocks)):
            ctr_enc = encrypt(str(ctr + i), key)
            block = [(i ^ j) for (i, j) in zip(ctr_enc, blocks[i])]
            ciphertext.append(block)

        ct = ''
        for i in range(len(ciphertext) - 1, 0, -1):
            for j in range(len(ciphertext[i])):
                ct += str(ciphertext[i][j])
        print('Cipher text: ', ct)
        return ciphertext

    def ctr_decrypt(ciphertext, key):
        plaintext = []
        ctr = ciphertext[0]
        k = 0
        for i in range(1, len(ciphertext)):
            ctr_enc = encrypt(str(ctr + k), key)
            block = [(i ^ j) for (i, j) in zip(ctr_enc, ciphertext[i])]
            plaintext.append(block)
            k += 1
        pl = ''
        for i in range(len(plaintext)):
            for j in range(len(plaintext[i])):
                pl += str(plaintext[i][j])
        return pl

    if process == 'encrypt':
        text = ctr_encrypt(text, key)
    else:
        text = ctr_decrypt(text, key)
    return text


if __name__ == '__main__':
    print("CBC mode:\n")
    pt = '7978964654646456787464523464651802013134684612310345643126123546'
    print("Plain text: ", pt)
    k = '7564906748398462'
    print('Used key: ', k)
    ct = cbc('encrypt', pt, k)
    pl = cbc('decrypt', ct, k)
    print("Decrypted text: ", pl)

    print("\nCTR mode:\n")
    print("Plain text: ", pt)
    print('Used key: ', k)
    ct = ctr('encrypt', pt, k)
    print("Decrypted text: ", ctr('decrypt', ct, k))
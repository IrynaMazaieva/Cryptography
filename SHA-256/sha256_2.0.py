from func2_0 import *
from consts import *


def sha_256(input_string):
    w_t = message_parsing(input_string)
    a = binary_32bit(decimal_return_hex(str(H[0])))
    b = binary_32bit(decimal_return_hex(str(H[1])))
    c = binary_32bit(decimal_return_hex(str(H[2])))
    d = binary_32bit(decimal_return_hex(str(H[3])))
    e = binary_32bit(decimal_return_hex(str(H[4])))
    f = binary_32bit(decimal_return_hex(str(H[5])))
    g = binary_32bit(decimal_return_hex(str(H[6])))
    h = binary_32bit(decimal_return_hex(str(H[7])))
    for i in range(0, 64):
        if i <= 15:
            t_1 = mod_32_addition([int(h, 2), int(e_1(e), 2), int(Ch(e, f, g), 2), int(str(K[i]), 16), int(w_t[i], 2)])
            t_2 = mod_32_addition([int(e_0(a), 2), int(Maj(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = mod_32_addition([int(d, 2), t_1])
            d = c
            c = b
            b = a
            a = mod_32_addition([t_1, t_2])
            a = binary_32bit(a)
            e = binary_32bit(e)
        if i > 15:
            w_t.append(message_schedule(i, w_t))
            t_1 = mod_32_addition([int(h, 2), int(e_1(e), 2), int(Ch(e, f, g), 2), int(str(K[i]), 16), int(w_t[i], 2)])
            t_2 = mod_32_addition([int(e_0(a), 2), int(Maj(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = mod_32_addition([int(d, 2), t_1])
            d = c
            c = b
            b = a
            a = mod_32_addition([t_1, t_2])
            a = binary_32bit(a)
            e = binary_32bit(e)
    hash_0 = mod_32_addition([decimal_return_hex(str(H[0])), int(a, 2)])
    hash_1 = mod_32_addition([decimal_return_hex(str(H[1])), int(b, 2)])
    hash_2 = mod_32_addition([decimal_return_hex(str(H[2])), int(c, 2)])
    hash_3 = mod_32_addition([decimal_return_hex(str(H[3])), int(d, 2)])
    hash_4 = mod_32_addition([decimal_return_hex(str(H[4])), int(e, 2)])
    hash_5 = mod_32_addition([decimal_return_hex(str(H[5])), int(f, 2)])
    hash_6 = mod_32_addition([decimal_return_hex(str(H[6])), int(g, 2)])
    hash_7 = mod_32_addition([decimal_return_hex(str(H[7])), int(h, 2)])
    final_hash = (hex_return(hash_0),
                  hex_return(hash_1),
                  hex_return(hash_2),
                  hex_return(hash_3),
                  hex_return(hash_4),
                  hex_return(hash_5),
                  hex_return(hash_6),
                  hex_return(hash_7))
    s = ''
    for i in final_hash:
        s += str(i)
    return s

def hmac(plaintext, key):
    if len(key)*8 < 512:
        key = (512//8 - len(key))*'0' + key
    elif len(key)*8 > 512:
        key = sha_256(key)

    ipad = '0x36'*16
    opad = '0x5c'*16
    ikeypad = xor_2str(message_bit_return(ipad), message_bit_return(key))
    okeypad = xor_2str(message_bit_return(opad), message_bit_return(key))
    return str(sha_256(okeypad)) + str(sha_256(ikeypad)) + plaintext




# -----1------

t = input()
hsh = sha_256(t)
print("SHA-126 hash: ", hsh)

# -----2------

key_for_aes128 = 'key for aes 128'
key_for_aes128 = sha_256(key_for_aes128)[:16]
print("Key for AES-128: ", key_for_aes128)
print("Length of the key in bits: ", len(key_for_aes128)*8)

# ------3-------
k = 'ifashvknfusfjl998jmkl'
t = 'qwertyuiop234567890asdfghjkl'
print("Key: ", k)
print("Text: ", t)
print("HMAC result: ", hmac(t, k))



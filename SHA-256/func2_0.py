def binary_return(decimal):
    return str(format(decimal, 'b'))


def binary_8bit(decimal):
    return str(format(decimal, '08b'))


def binary_32bit(decimal):
    return str(format(decimal, '032b'))


def binary_64bit(decimal):
    return str(format(decimal, '064b'))


def hex_return(decimal):
    return str(format(decimal, 'x'))


def decimal_return_binary(binary_string):
    return int(binary_string, 2)


def decimal_return_hex(hex_string):
    return int(hex_string, 16)


def L_P(mass, n):
    to_return = []
    j = 0
    k = n
    while k < len(mass) + 1:
        to_return.append(mass[j:k])
        j = k
        k += n
    return to_return


def s_l(bit_string):
    bit_list = []
    for i in range(len(bit_string)):
        bit_list.append(bit_string[i])
    return bit_list


def l_s(bit_list):
    bit_string = ''
    for i in range(len(bit_list)):
        bit_string += bit_list[i]
    return bit_string


def rotate_right(bit_string, n):
    bit_list = s_l(bit_string)
    count = 0
    while count <= n - 1:
        list_main = list(bit_list)
        var_0 = list_main.pop(-1)
        list_main = list([var_0] + list_main)
        bit_list = list(list_main)
        count += 1
    return l_s(list_main)


def shift_right(bit_string, n):
    bit_list = s_l(bit_string)
    count = 0
    while count <= n - 1:
        bit_list.pop(-1)
        count += 1
    front_append = ['0'] * n
    return l_s(front_append + bit_list)


def mod_32_addition(input_mass):
    value = 0
    for i in range(len(input_mass)):
        value += input_mass[i]
    mod_32 = 4294967296  # 2^32
    return value % mod_32


def xor_2str(bit_string_1, bit_string_2):
    xor_list = []

    if len(bit_string_1) != len(bit_string_2):
        if len(bit_string_1) > len(bit_string_2):
            bit_string_2 = '0'*(len(bit_string_1) - len(bit_string_2)) + bit_string_2
        else:
            bit_string_1 = '0' * (len(bit_string_2) - len(bit_string_1)) + bit_string_1

    for i in range(len(bit_string_1)):
        if bit_string_1[i] == '0' and bit_string_2[i] == '0':
            xor_list.append('0')
        if bit_string_1[i] == '1' and bit_string_2[i] == '1':
            xor_list.append('0')
        if bit_string_1[i] == '0' and bit_string_2[i] == '1':
            xor_list.append('1')
        if bit_string_1[i] == '1' and bit_string_2[i] == '0':
            xor_list.append('1')
    return l_s(xor_list)


def and_2str(bit_string_1, bit_string_2):
    and_list = []

    if len(bit_string_1) != len(bit_string_2):
        if len(bit_string_1) > len(bit_string_2):
            bit_string_2 = '0'*(len(bit_string_1) - len(bit_string_2)) + bit_string_2
        else:
            bit_string_1 = '0' * (len(bit_string_2) - len(bit_string_1)) + bit_string_1

    for i in range(len(bit_string_1)):
        if bit_string_1[i] == '1' and bit_string_2[i] == '1':
            and_list.append('1')
        else:
            and_list.append('0')

    return l_s(and_list)


def or_2str(bit_string_1, bit_string_2):
    or_list = []

    if len(bit_string_1) != len(bit_string_2):
        if len(bit_string_1) > len(bit_string_2):
            bit_string_2 = '0'*(len(bit_string_1) - len(bit_string_2)) + bit_string_2
        else:
            bit_string_1 = '0' * (len(bit_string_2) - len(bit_string_1)) + bit_string_1

    for i in range(len(bit_string_1)):
        if bit_string_1[i] == '0' and bit_string_2[i] == '0':
            or_list.append('0')
        else:
            or_list.append('1')
    return l_s(or_list)


def not_str(bit_string):
    not_list = []
    for i in range(len(bit_string)):
        if bit_string[i] == '0':
            not_list.append('1')
        else:
            not_list.append('0')
    return l_s(not_list)


def Ch(x, y, z):
    return xor_2str(and_2str(x, y), and_2str(not_str(x), z))


def Maj(x, y, z):
    return xor_2str(xor_2str(and_2str(x, y), and_2str(x, z)), and_2str(y, z))


def e_0(x):
    return xor_2str(xor_2str(rotate_right(x, 2), rotate_right(x, 13)), rotate_right(x, 22))


def e_1(x):
    return xor_2str(xor_2str(rotate_right(x, 6), rotate_right(x, 11)), rotate_right(x, 25))


def s_0(x):
    return xor_2str(xor_2str(rotate_right(x, 7), rotate_right(x, 18)), shift_right(x, 3))


def s_1(x):
    return xor_2str(xor_2str(rotate_right(x, 17), rotate_right(x, 19)), shift_right(x, 10))


def message_pad(bit_list):
    pad_one = bit_list + '1'
    pad_len = len(pad_one)
    k = 0
    while ((pad_len + k) - 448) % 512 != 0:
        k += 1
    back_append_0 = '0' * k
    back_append_1 = binary_64bit(len(bit_list))
    return pad_one + back_append_0 + back_append_1


def message_bit_return(string_input):
    bit_list = []
    for i in range(len(string_input)):
        bit_list.append(binary_8bit(ord(string_input[i])))
    return l_s(bit_list)


def message_pre_pro(input_string):
    bit_main = message_bit_return(input_string)
    return message_pad(bit_main)


def message_parsing(input_string):
    return L_P(message_pre_pro(input_string), 32)


def message_schedule(index, w_t):
    new_word = binary_32bit(mod_32_addition([int(s_1(w_t[index - 2]), 2), int(w_t[index - 7], 2), int(s_0(w_t[index - 15]), 2), int(w_t[index - 16], 2)]))
    return new_word



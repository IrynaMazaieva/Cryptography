ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'


def encrypt(text, key):
    encrypted = ""
    ciphertext = ''
    text = text.lower()
    for i in range(len(text)):
        if text[i] in ALPHABET:
            ciphertext += text[i]

    key_string = key * ((len(ciphertext) // len(key)) + 1)
    for i in range(len(ciphertext)):
        index = ALPHABET.index(ciphertext[i]) + ALPHABET.index(key_string[i])
        if index > 32:
            index -= 33
        encrypted += ALPHABET[index]
    return encrypted


def decrypt(text, key):
    decrypted = ""
    key_string = key * ((len(text) // len(key)) + 1)
    for i in range(len(text)):
        index = ALPHABET.index(text[i]) - ALPHABET.index(key_string[i])
        if index < 0:
            index += 33
        decrypted += ALPHABET[index]
    return decrypted


if __name__ == '__main__':
    f = open('HarriPotter.txt', encoding='utf-8')
    f = f.read()
    output = open('HarriPotterEncrypted.txt', 'x', encoding='utf-8')

    output.write(encrypt(f, 'северусснейп'))

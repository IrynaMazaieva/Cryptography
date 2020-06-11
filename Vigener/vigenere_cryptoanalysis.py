from vigenere_cipher import decrypt
from ukrainian_letter_frequences import UKRAINIAN_LETTER_FREQUENCES
from scipy.stats import chisquare

ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
EXPECTED = 0.04984338411945382


def get_letter_count(text):
    letter_count = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'ґ': 0, 'д': 0, 'е': 0, 'є': 0, 'ж': 0, 'з': 0, 'и': 0,
                    'і': 0, 'ї': 0, 'й': 0, 'к': 0, 'л': 0, 'м': 0, 'н': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0,
                    'т': 0, 'у': 0, 'ф': 0, 'х': 0, 'ц': 0, 'ч': 0, 'ш': 0, 'щ': 0, 'ю': 0, 'я': 0, 'ь': 0}

    for i in range(len(text)):
        letter_count[text[i]] += 1
    return letter_count


def get_expected_key(text, key_length):
    k = [' '] * key_length
    text_parts = []
    for i in range(key_length):
        text_parts.append(text[i::key_length])
    for i in range(len(text_parts)):
        value = 1e11
        for letter in ALPHABET:
            chi_2 = chisquare(list(get_letter_count(decrypt(text_parts[i], letter)).values()), \
                              list(UKRAINIAN_LETTER_FREQUENCES.values()))[0]
            if chi_2 < value:
                value = chi_2
                k[i] = letter
    key = ''
    for i in k:
        key += i
    return key


def index_of_coincidences(text, key_length):
    i_c = 0
    n = len(text[:: key_length])
    if n <= 1:
        return 0
    letter_count = get_letter_count(text[:: key_length])
    for i in letter_count.keys():
        i_c += letter_count[i] * (letter_count[i] - 1)
    i_c = i_c / (n * (n - 1))
    return i_c


def analyze_encrypted_text(text):
    cipher_text = text.lower()
    for i in range(len(text)):
        if text[i] in ALPHABET:
            cipher_text += text[i]

    print("Шукаємо оптимальну довжину ключа:")
    ans = [1e9]
    for key_length in range(1, len(ALPHABET)):
        ans.append((index_of_coincidences(cipher_text, key_length) - EXPECTED)**2)
    key_length = ans.index(min(ans))
    print(key_length, "- найкраща довжина ключа.")
    print('Шукаємо вірогідний ключ:')
    key = get_expected_key(cipher_text, key_length)
    print('ключ підібрано - ', key)
    proposed = decrypt(cipher_text, key)
    return proposed


if __name__ == "__main__":
    text = open('HarriPotterEncrypted.txt', encoding='utf-8').read(30000)
    output = open('HarriPotterDecrypted.txt', 'w', encoding='utf-8').write(analyze_encrypted_text(text))

import this

cipher = this.s
dictionary = this.d

def decipher(text, translator):
    translation = ""
    for letter in text.strip():
        translation += translator.get(letter, letter)
    return translation


if __name__ == '__main__':
    print(decipher(cipher, dictionary))
    print(cipher)


from sys import argv

from adfgx import encrypt, decrypt


def main(polybius_key, column_key):
    while True:
        direction = safe_input("[E]ncrypt/[D]ecrypt? ([Q] to quit) ")
        if direction[0].upper() == 'E':
            plaintext = input("Plaintext message? ")
            print(encrypt(plaintext, polybius_key, column_key))
        elif direction[0].upper() == 'D':
            ciphertext = input("Ciphertext Message? ")
            print(decrypt(ciphertext, polybius_key, column_key))
        elif direction[0].upper() == 'Q':
            print("Goodbye!")
            exit()
        else:
            print("I didn't understand, please try again")


def safe_input(prompt):
    user_input = ''
    while not user_input:
        try:
            user_input = input(prompt)
            if not user_input:
                print("No input received.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()
    return user_input


if __name__ == '__main__':
    if not len(argv) > 2:
        print("Need two keys!")
        exit(1)
    main(*argv[1:])
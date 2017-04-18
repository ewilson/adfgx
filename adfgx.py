from collections import defaultdict

alphabet = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'


def encrypt(plaintext, polybius_key, column_key):
    fract = plaintext_to_fract(plaintext, polybius_key)
    return fract_to_ciphertext(fract, column_key)


def decrypt(ciphertext, polybius_key, column_key):
    fract = ciphertext_to_fract(ciphertext, column_key)
    return fract_to_plaintext(fract, polybius_key)


class Polybius:
    """
    Polybius is a grid the fractionates the input plaintext into pairs of characters
    """

    def __init__(self, key_phrase=None):
        """
        :param key_phrase: determins order of letters in 5x5 grid
        """
        if key_phrase is None:
            self.alpha = alphabet
        else:
            clean_phrase = clean(key_phrase, merge_ij=True)
            deduped_phrase = dedup(clean_phrase)
            new_alphabet = scramble_alphabet(deduped_phrase)
            self.alpha = new_alphabet
        self.adfgx = 'ADFGX'

    def to_fract(self, letter):
        index = self.alpha.index(letter)
        return self.adfgx[index // 5] + self.adfgx[index % 5]

    def to_plaintext(self, pair):
        row = self.adfgx.index(pair[0])
        col = self.adfgx.index(pair[1])
        return self.alpha[5*row + col]


class ColTrans:
    """
    Column transformation class takes fractionated text in rows, and returns
    them by columns -- transformed, based on the trans_key
    """

    def __init__(self, trans_key):
        clean_phrase = clean(trans_key)
        deduped_phrase = dedup(clean_phrase)
        self.trans_key = deduped_phrase
        self.columns = defaultdict(lambda: [])
        self.key_len = len(self.trans_key)

    def fill(self, fract):
        for idx, letter in enumerate(fract):
            key = self.trans_key[idx % self.key_len]
            self.columns[key].append(letter)

    def reverse_fill(self):
        orig = []
        num = 0
        while True:
            letter = self.trans_key[num % self.key_len]
            current_column = self.columns[letter]
            if not current_column:
                break
            orig.append(current_column.pop(0))
            num += 1
        return ''.join(orig)

    def dump(self):
        out = []
        for key in sorted(self.trans_key):
            out.extend(self.columns[key])
        return ''.join(out)

    def reverse_dump(self, ciphertext):
        remainder = len(ciphertext) % self.key_len
        base_height = len(ciphertext) // self.key_len
        cipher_chars = list(ciphertext)
        for letter in sorted(self.trans_key):
            height = base_height + 1 if self.trans_key.index(letter) < remainder else base_height
            self.columns[letter].extend(cipher_chars[0:height])
            cipher_chars = cipher_chars[height:]


def plaintext_to_fract(phrase, key_phrase=''):
    polybius = Polybius(key_phrase)
    cleaned_phrase = clean(phrase, merge_ij=True)
    pairs = [polybius.to_fract(c) for c in cleaned_phrase]
    return ''.join(pairs)


def fract_to_plaintext(fract, polybius_key):
    polybius = Polybius(polybius_key)
    fract_chars = list(fract)
    plaintext = ''
    while fract_chars:
        plaintext += polybius.to_plaintext(fract_chars[:2])
        fract_chars = fract_chars[2:]
    return plaintext


def fract_to_ciphertext(fract, column_key):
    coltrans = ColTrans(column_key)
    coltrans.fill(fract)
    return coltrans.dump()


def ciphertext_to_fract(ciphertext, column_key):
    coltrans = ColTrans(column_key)
    coltrans.reverse_dump(ciphertext)
    return coltrans.reverse_fill()


def scramble_alphabet(phrase):
    return phrase + ''.join([c for c in alphabet if c not in phrase])


def dedup(phrase):
    return ''.join(list(dict.fromkeys(phrase)))


def clean(phrase, merge_ij=False):
    coalesce = (lambda c: 'J' if c == 'I' else c) if merge_ij else lambda c: c
    uppercase_no_punct = [c.upper() for c in phrase if c.isalpha()]
    return ''.join([coalesce(c) for c in uppercase_no_punct])



from main import *


def test_clean_merge_ij():
    phrase = "The dry fish swims, alone!"

    assert "THEDRYFJSHSWJMSALONE" == clean(phrase, merge_ij=True)


def test_clean_no_merge():
    phrase = "dry fish!"

    assert "DRYFISH" == clean(phrase)


def test_dedup():
    phrase = 'THEDRYFJSHSWJMSALONE'

    assert 'THEDRYFJSWMALON' == dedup(phrase)


def test_scramble_alphabet():
    phrase = 'THEDRYFJSWMALON'

    assert 'THEDRYFJSWMALONBCGKPQUVXZ' == scramble_alphabet(phrase)


def test_to_fract():
    polybius = Polybius()

    assert 'AA' == polybius.to_fract('A')
    assert 'AD' == polybius.to_fract('B')
    assert 'AX' == polybius.to_fract('E')
    assert 'DA' == polybius.to_fract('F')
    assert 'DD' == polybius.to_fract('G')
    assert 'FF' == polybius.to_fract('N')
    assert 'XX' == polybius.to_fract('Z')


def test_to_plaintext():
    polybius = Polybius()

    assert 'A' == polybius.to_plaintext('AA')
    assert 'B' == polybius.to_plaintext('AD')
    assert 'E' == polybius.to_plaintext('AX')
    assert 'F' == polybius.to_plaintext('DA')
    assert 'G' == polybius.to_plaintext('DD')
    assert 'N' == polybius.to_plaintext('FF')
    assert 'Z' == polybius.to_plaintext('XX')


def test_default_alpha():
    polybius = Polybius()

    assert polybius.alpha == alphabet


def test_polybius_alphabet():
    polybius = Polybius("The dry fish swims alone!")

    assert polybius.alpha == 'THEDRYFJSWMALONBCGKPQUVXZ'


def test_first_part():
    assert 'AAGGGGAAAFDXAAGGAGAAXDFF' == plaintext_to_fract('Attack at dawn!')


def test_coltrans():
    coltrans = ColTrans('blue jackets')

    assert coltrans.trans_key == 'BLUEJACKTS'


def test_fill():
    coltrans = ColTrans('LOGAN')

    coltrans.fill("ABCDEFGHIJKLM")

    assert coltrans.columns['L'] == ['A', 'F', 'K']
    assert coltrans.columns['O'] == ['B', 'G', 'L']
    assert coltrans.columns['G'] == ['C', 'H', 'M']
    assert coltrans.columns['A'] == ['D', 'I']
    assert coltrans.columns['N'] == ['E', 'J']


def test_dump():
    coltrans = ColTrans('LOGAN')
    coltrans.columns = {
        'L': ['A', 'F', 'K'],
        'O': ['B', 'G', 'L'],
        'G': ['C', 'H', 'M'],
        'A': ['D', 'I'],
        'N': ['E', 'J'],
    }

    ciphertext = coltrans.dump()

    assert ciphertext == 'DICHMAFKEJBGL'


def test_encrypt():
    ciphertext = encrypt(
        'report to headquarters immediately after dark',
        'dry fish swimming alone',
        'elixir'
    )

    assert ciphertext == 'AGXGFXAXAGAAAGADFGXDADXDDXFXFAADDFADDXDAXFXFFXDAGDFXGDFADAXFAXFFXAAFAFADGADFDFAG'


def test_decrypt():
    plaintext = decrypt(
        'AGXGFXAXAGAAAGADFGXDADXDDXFXFAADDFADDXDAXFXFFXDAGDFXGDFADAXFAXFFXAAFAFADGADFDFAG',
        'dry fish swimming alone',
        'elixir'
    )

    assert 'REPORTTOHEADQUARTERSJMMEDJATELYAFTERDARK' == plaintext


def test_reverse_fill():
    ciphertext = 'ABCDEFG'
    coltrans = ColTrans('yak')

    coltrans.reverse_dump(ciphertext)

    assert coltrans.columns['A'] == ['A', 'B']
    assert coltrans.columns['K'] == ['C', 'D']
    assert coltrans.columns['Y'] == ['E', 'F', 'G']


def test_reverse_dump():
    coltrans = ColTrans('LOGAN')
    coltrans.columns = {
        'L': ['A', 'F', 'K'],
        'O': ['B', 'G', 'L'],
        'G': ['C', 'H', 'M'],
        'A': ['D', 'I'],
        'N': ['E', 'J'],
    }

    assert coltrans.reverse_fill() == 'ABCDEFGHIJKLM'
#!/usr/bin/env python3

SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B


def step(x):
    x = (x & 1) << N+1 | x << 1 | x >> N-1
    y = 0
    for i in range(N):
        y |= SUB[(x >> i) & 7] << i
    return y


def int_to_bytes(x):
    return x.to_bytes(N_B, byteorder='little')


def bytes_to_int(b):
    return int.from_bytes(b, byteorder='little')


with open('in/bis.txt', 'rb') as bisTxt:
    bisTxtFile = bisTxt.read()
with open('in/bis.txt.enc', 'rb') as bisTxtEnc:
    bisTxtEncFile = bisTxtEnc.read()
with open('in/super_cipher.py.enc', 'rb') as superCipherEnc:
    superCipherEncFile = superCipherEnc.read()
with open('in/hint.gif.enc', 'rb') as hintEnc:
    hintFile = hintEnc.read()

key = bytes([(a ^ b) for a, b in zip(bisTxtFile, bisTxtEncFile)])

superCipherPart = bytes([(a ^ b) for a, b in zip(superCipherEncFile, key)])

while len(key) <= len(superCipherEncFile):
    tmp = int.from_bytes(key[-32:], byteorder='little')
    key = key + int.to_bytes(step(tmp), N_B, byteorder='little')

superCipher = bytes([(a ^ b) for a, b in zip(superCipherEncFile, key)])

while len(key) <= len(hintFile):
    tmp = int.from_bytes(key[-32:], byteorder='little')
    key = key + int.to_bytes(step(tmp), N_B, byteorder='little')

hint = bytes([(a ^ b) for a, b in zip(hintFile, key)])


def rotate_left(x):
    part1 = (x & (2 ** N - 1)) >> 1
    part2 = (x & 1) << (N - 1)
    x_prev = (part1 | part2) & ((2 ** 256) - 1)
    return x_prev


# if 0 - 000 / 011 / 101 / 111
# if 1 - 001 / 010 / 100 / 110
def getDefaultX(xModified):
    bit = (xModified >> N - 1) & 1
    if bit == 0:
        one = 0
        two = 3
        three = 5
        four = 7
    elif bit == 1:
        one = 1
        two = 2
        three = 4
        four = 6
    else:
        raise Exception("wrong bit")

    for i in range(N - 1):
        bit = xModified >> (N - 2 - i) & 1
        one_last2 = one & 3
        two_last2 = two & 3
        three_last2 = three & 3
        four_last2 = four & 3
        if bit == 0:
            if one_last2 == 0:
                one = (one << 1) + 0
            elif one_last2 == 1:
                one = (one << 1) + 1
            elif one_last2 == 2:
                one = (one << 1) + 1
            elif one_last2 == 3:
                one = (one << 1) + 1

            if two_last2 == 0:
                two = (two << 1) + 0
            elif two_last2 == 1:
                two = (two << 1) + 1
            elif two_last2 == 2:
                two = (two << 1) + 1
            elif two_last2 == 3:
                two = (two << 1) + 1

            if three_last2 == 0:
                three = (three << 1) + 0
            elif three_last2 == 1:
                three = (three << 1) + 1
            elif three_last2 == 2:
                three = (three << 1) + 1
            elif three_last2 == 3:
                three = (three << 1) + 1

            if four_last2 == 0:
                four = (four << 1) + 0
            elif four_last2 == 1:
                four = (four << 1) + 1
            elif four_last2 == 2:
                four = (four << 1) + 1
            elif four_last2 == 3:
                four = (four << 1) + 1
        # if 0 - 000 / 011 / 101 / 111
        # if 1 - 001 / 010 / 100 / 110
        elif bit == 1:
            if one_last2 == 0:
                one = (one << 1) + 1
            elif one_last2 == 1:
                one = (one << 1) + 0
            elif one_last2 == 2:
                one = (one << 1) + 0
            elif one_last2 == 3:
                one = (one << 1) + 0

            if two_last2 == 0:
                two = (two << 1) + 1
            elif two_last2 == 1:
                two = (two << 1) + 0
            elif two_last2 == 2:
                two = (two << 1) + 0
            elif two_last2 == 3:
                two = (two << 1) + 0

            if three_last2 == 0:
                three = (three << 1) + 1
            elif three_last2 == 1:
                three = (three << 1) + 0
            elif three_last2 == 2:
                three = (three << 1) + 0
            elif three_last2 == 3:
                three = (three << 1) + 0

            if four_last2 == 0:
                four = (four << 1) + 1
            elif four_last2 == 1:
                four = (four << 1) + 0
            elif four_last2 == 2:
                four = (four << 1) + 0
            elif four_last2 == 3:
                four = (four << 1) + 0

    one = rotate_left(one)
    two = rotate_left(two)
    three = rotate_left(three)
    four = rotate_left(four)

    one_modif = step(one)
    two_modif = step(two)
    three_modif = step(three)
    four_modif = step(four)

    if one_modif == xModified:
        return one
    elif two_modif == xModified:
        return two
    elif three_modif == xModified:
        return three
    elif four_modif == xModified:
        return four
    else:
        raise Exception("Something went wrong")


old_x = 0
x = bytes_to_int(key[0:32])

for i in range(N//2):
    old_x = getDefaultX(x)
    x = old_x

x = x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')
print(x.decode(), end='')

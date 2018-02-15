from binascii import hexlify, unhexlify
import math


def mySum(*args):
    total = 0
    for arg in args:
        total += arg
    return total


def bitget(valIn, startBit, stopBit):
    mask = 0
    for ii in range(startBit, stopBit+1):
        mask += 2**ii
    bitsRtn = (valIn & mask) >> startBit
    return bin(bitsRtn)


def a2h(dataIn):
    return hexlify(bytes(dataIn, 'utf-8'))


def h2a(dataIn):
    return unhexlify("{0:0X}".format(dataIn))


def eng_string(x, sigFigs, format='%s', resFormat='engineering'):
    '''
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.

    E.g. with format='%.2f':
        1.23e-08 => 12.30e-9
             123 => 123.00
          1230.0 => 1.23e3
      -1230000.0 => -1.23e6

    and with si=True:
          1230.0 => 1.23k
      -1230000.0 => -1.23M
    '''
    if ((resFormat == 'si') or (resFormat == 'engineering')):
        sign = ''
        if x < 0:
            x = -x
            sign = '-'
        exp = int(math.floor(math.log10(x)))
        exp3 = exp - (exp % 3)
        x3 = x / (10 ** exp3)

        if (resFormat == 'si') and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
            exp3_text = 'yzafpnum kMGTPEZY'[int(math.floor((exp3 - (-24)) / 3))]
        elif exp3 == 0:
            exp3_text = ''
        else:
            exp3_text = 'e%s' % exp3

        x3 = '{0:.{digits}g}'.format(x3, digits=sigFigs)
        result = ('%s' % sign) + x3 + ('%s' % exp3_text)
    else:
        result = '{0:.{digits}g}'.format(x, digits=sigFigs)

    return result

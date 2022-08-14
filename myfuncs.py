from binascii import hexlify, unhexlify
import math
from resistors import res1Per, resp1Per


def mySum(*args):
    total = 0
    for arg in args:
        total += arg
    return total


def bitget(valIn, stopBit, startBit):
    mask = 0
    for ii in range(startBit, stopBit+1):
        mask += 2**ii
    bitsRtn = (valIn & mask) >> startBit
    return bin(bitsRtn)


def a2h(dataIn):
    return hexlify(bytes(dataIn, 'utf-8'))


def h2a(dataIn):
    return unhexlify("{0:0X}".format(dataIn))


def findres(target_r, tol=1):
    if (tol == 0.1):
        resList = resp1Per
    else:
        resList = res1Per

    # Find multiplier
    multiplier = 0
    for ii in range(0, 6):
        if (target_r < 100):
            break
        else:
            target_r = target_r/10
            multiplier = multiplier + 1

    closestMatch = 0
    diff = 200

    for ii in range(0, len(resList)):
        if (abs(resList[ii] - target_r) < diff):
            closestMatch = resList[ii]
            diff = abs(resList[ii] - target_r)
    return closestMatch*10**multiplier


def vdiv(vin, r1, r2):
    return vin - vin/(r1+r2)*r1


def rpar(*argv):
    sum = 0
    for arg in argv:
        sum = sum + 1/arg
    return 1/sum


def findrdiv(vin, vout, tol=1):
    if (tol == .1):
        resistors = resp1Per
    else:
        resistors = res1Per

    resistorsBig = resistors + resistors*10 + resistors*100 + resistors*1000

    ratio = vout/vin
    matchR1 = 0
    matchR2 = 0
    bestDiff = 1e6

    if (ratio <= .5):
        for ii in range(0, len(resistors)):
            for jj in reversed(range(ii, len(resistorsBig))):
                newRatio = resistors[ii]/(resistorsBig[jj]+resistors[ii])
                diff = abs(newRatio - ratio)
                if (diff < bestDiff):
                    bestDiff = diff
                    matchR1 = resistorsBig[jj]
                    matchR2 = resistors[ii]  
    else:
        for ii in range(0, len(resistorsBig)):
            for jj in range(0, len(resistors)):
                newRatio = resistorsBig[ii]/(resistors[jj]+resistorsBig[ii])
                diff = abs(newRatio - ratio)
                if (diff < bestDiff):
                    bestDiff = diff
                    matchR1 = resistors[jj]
                    matchR2 = resistorsBig[ii]
    return [matchR1, matchR2]


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

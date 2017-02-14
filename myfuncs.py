from binascii import hexlify,unhexlify

def mySum(*args):
    total = 0
    for arg in args:
        total += arg
    return total

def bitget(valIn,startBit,stopBit):
    mask = 0
    for ii in range(startBit,stopBit+1):
        mask += 2**ii
    bitsRtn = (valIn & mask) >> startBit
    return bin(bitsRtn)

def a2h(dataIn):
    return hexlify(bytes(dataIn,'utf-8'))

def h2a(dataIn):
    return unhexlify("{0:0X}".format(dataIn))
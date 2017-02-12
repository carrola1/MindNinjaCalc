
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

def a2h(*args):
    hexOut = (", ".join("{:02x}".format(arg) for arg in args))
    return hexOut

def a2h(strIn):
    return strIn.decode("hex")
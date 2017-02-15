import re

key = 'x'
newKey = 'y'
operators = ['+','-','/']
patStr = key + '(?=[' + ''.join(operators) + '])'  #r'(' + key + ' )|
replStr = newKey

x = re.sub(patStr,replStr, r'x+5')
print(patStr)
print(replStr)
print(x)
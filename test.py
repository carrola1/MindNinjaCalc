import re

x = re.sub('(\d)(u)','\g<1>*10**-6', '5 u')

y = 2e-6

print(y)
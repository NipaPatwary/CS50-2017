import cs50
import sys

# check for proper usage
if len(sys.argv) != 2:
    print('Usage: caesar.py key')
    exit(1)

# convert first argument (key) to integer
key = int(sys.argv[1])

# get plaintext
print('plaintext: ', end = '')
plain = cs50.get_string()

print('ciphertext: ', end = '')
# check for each letter in plaintext if it's alphabetical, lower or upper
# and print adequate ciphertext
for c in plain:
    if c.isalpha():
        if c.islower():
            if ord(c) + key > 122:
                temp = (ord(c) - 97 + key) % 26
                print(chr(temp + 97), end = '')
            else:
                temp = ord(c) + key
                print(chr(temp), end = '')
        elif c.isupper():
            if ord(c) + key > 90:
                temp = (ord(c) - 65 + key) % 26
                print(chr(temp + 65), end = '')
            else:
                temp = ord(c) + key
                print(chr(temp), end = '')
    else:
        print(c, end = '')

print()
exit(0)
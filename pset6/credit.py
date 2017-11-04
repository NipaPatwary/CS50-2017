import cs50

# get credit card number
print('Number: ', end='')
cc_num = cs50.get_int()

sum1 = 0
sum2 = 0
i = cc_num
j = cc_num // 10

# implement Luhn algorothm
# calculate sum of every second number, starting from the last
while i > 0:
    sum1 += i % 10
    i //= 100

# calculate sum of every second number's digits multiplied by 2, starting from second last
while j > 0:
    if j % 10 * 2 < 9:
        sum2 += j % 10 * 2
    else:
        sum2 += (j % 10 * 2) // 10 + (j % 10 * 2) % 10
    j //= 100

# check if credit card number is valid and determine type of the card
if (sum1 + sum2) % 10 == 0:
    if cc_num // 10000000000000 == 34 or cc_num // 10000000000000 == 37:
        print('AMEX')
    elif cc_num // 100000000000000 > 50 and cc_num // 100000000000000 < 56:
        print('MASTERCARD')
    elif cc_num // 1000000000000 == 4 or cc_num // 1000000000000000 == 4:
        print('VISA')
else:
        print('INVALID')
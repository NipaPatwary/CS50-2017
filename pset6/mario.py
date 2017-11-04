import cs50

# prompt user to enter height that is in range of 1 - 23
while True:
    print('Height: ', end='')
    height = cs50.get_int()
    if height > 0 and height <= 23:
        break

for i in range(height):                     # for each row
    print(' ' * (height - i - 1), end='')   # print blanks
    print('#' * (i + 1), end='')            # print bricks
    print('  ', end='')                     # print gap
    print('#' * (i + 1))                    # finish the row with bricks and newline
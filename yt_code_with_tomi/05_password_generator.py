import random

print('Welcome to your Password Generator\n')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().;?0123456789'

amount = input('Amount of passwords to generate: ')
amount = int(amount)
length = input('Length of your password: ')
length = int(length)

print('\nHere are your passwords:\n')

for pwd in range(amount):
    passwords = ''
    for c in range(length):
        passwords += random.choice(chars)
    print(passwords)

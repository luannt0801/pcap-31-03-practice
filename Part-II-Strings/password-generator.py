import random

alpha = "abcdefghijklmnopqrstuvwxyz"
num = "0123456789"
special = "!@#$%&*^|()_+"

def get_available_chars(include_digits, include_special):
    available_chars = alpha
    if include_digits:
        available_chars += num
    if include_special:
        available_chars += special
    return available_chars

def generate_password(length = 16, mixed_case = False, 
                      include_digits = False, include_special = False):
    password = []
    available_chars = get_available_chars(include_digits, include_special)
    
    for i in range(length):
        character = random.choice(available_chars)
        
        if mixed_case and character.isalpha():
            change_to_upper = random.randint(0, 1)
            if change_to_upper:
                character = character.upper()
                
        password.append(character)
    return ''.join(password)

def interact_main_menu():
    while True:
        print('\n-- Password generator --')
        print('Choose option:')
        print('1: generate password')
        print('2: exit the program')
        user_choice = input('Your choice: ')
        if user_choice == '1':
            interact_password_type()
        elif user_choice == '2':
            print('Bye!')
            break
        else:
            print('Please enter a correct value')

def interact_password_type():
    length = int(input('Provide password length: '))
    include_upper = input('Use uppercase letters? (y/n): ').lower().strip() == 'y'
    include_digits = input('Use digits? (y/n): ').lower().strip() == 'y'
    include_special = input('Use special characters? (y/n): ').lower().strip() == 'y'
    print('\nGenerated password:', generate_password(length, include_upper, include_digits, include_special))

if __name__ == '__main__':
    interact_main_menu()
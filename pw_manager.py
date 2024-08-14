# Thanks to AKX on StackOverflow for helping me with problems with the encrypt_data() and decrypt_data() functions (https://stackoverflow.com/questions/78798132/how-do-i-decrypt-a-cyphertext-encrypted-with-aes-with-pycryptodome?noredirect=1#comment138928412_78798132)

class bcolors:  # color codes for console text https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    header = '\033[34m'  # blue
    okblue = '\033[94m'  # bright blue
    okcyan = '\033[96m'  # bright cyan
    okgreen = '\033[92m'  # bright green
    warning = '\033[93m'  # bright yellow
    waitingInput = '\033[2m'  # dim
    fail = '\033[91m'  # bright red
    endc = '\033[0m'  # goes back to normal
    bold = '\033[1m'  # self explanatory
    underline = '\033[4m'  # self explanatory as well
    blink = '\033[5m'  # blinks slowly

import os
import time
from base64 import b64encode, b64decode
try:
    import json
except ModuleNotFoundError:
    os.system('pip install json' if os.name == 'nt' else 'pip3 install json')
    input(f'{bcolors.waitingInput}Press enter to continue{bcolors.endc}')
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    os.system('pip install tabulate' if os.name == 'nt' else 'pip3 install tabulate')
    input(f'{bcolors.waitingInput}Press enter to continue{bcolors.endc}')
try:
    import hashlib
except ModuleNotFoundError:
    os.system('pip install hashlib' if os.name == 'nt' else 'pip3 install hashlib')
    input(f'{bcolors.waitingInput}Press enter to continue{bcolors.endc}')
try:
    from Crypto.Cipher import AES
    from Crypto import Random
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Util.RFC1751 import english_to_key, key_to_english
except ModuleNotFoundError:
    os.system('pip install pycryptodome' if os.name == 'nt' else 'pip3 install pycryptodome')
    input(f'{bcolors.waitingInput}Press enter to continue{bcolors.endc}')

os.system('cls' if os.name == 'nt' else 'clear')

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_file = 'credentials.i_just_discovered_i_can_give_whatever_file_extension_i_want'  #can be opened with a text editor of your choice
iv = b'0000000000000000'

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def save_credentials(key, name, username, pw): # saves new credentials in the database
    credentials = []
    if os.path.exists(credentials_file):
        credentials = load_credentials()
    if len(credentials) == 0:
        credentials.append([len(credentials), name, username, pw])
    else:
        credentials.append([len(credentials), encrypt_data(key, name), encrypt_data(key, username), encrypt_data(key, pw)])
    with open(credentials_file, 'w') as file:
        json.dump(credentials, file, indent = 4)

def encrypt_data(key_bytes, plaintext):
    # print(f'{bcolors.okcyan}Encripting started{bcolors.endc}') # debug text
    # print(f'{bcolors.warning}Debug encrypt_data(1):\tpadded_key_bytes:\t{key_bytes}{bcolors.endc}') # debug text
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv)
    plaintext_bytes = plaintext.encode('utf-8')
    # print(f'{bcolors.warning}Debug encrypt_data(2):\tplaintext_bytes:\t{plaintext_bytes}{bcolors.endc}') # debug text
    padded_plaintext = pad(plaintext_bytes, AES.block_size)
    # print(f'{bcolors.warning}Debug encrypt_data(3):\tpadded_plaintext:\t{padded_plaintext}{bcolors.endc}') # debug text
    ciphertext_bytes = cipher.encrypt(padded_plaintext)
    # print(f'{bcolors.warning}Debug encrypt_data(4):\tciphertext_bytes:\t{ciphertext_bytes}{bcolors.endc}') # debug text
    ciphertext_str = b64encode(ciphertext_bytes).decode('utf-8')
    # print(f'{bcolors.warning}Debug encrypt_data(5):\tciphertext_str:\t\t{ciphertext_str}{bcolors.endc}') # debug text
    # print(f'{bcolors.okcyan}Encripting done{bcolors.endc}\n') # debug text
    return ciphertext_str

def signin(): # creates the json file that will store the main password and all the other passwords the first time the program is being run or if the file is moved or deleted
    credentials = False
    while not credentials:
        main_pw = input('Choose a main password to protect all of your other credentials: ')
        pw_confirm = input('Confirm your password: ')
        if main_pw == pw_confirm:
            save_credentials('Bitwarden at home', 'Bitwarden at home', 'sborra', sha256(main_pw))
            delete_lines(3)
            print(f'{bcolors.okgreen}\nYou correctly set your main password!{bcolors.endc}')
            time.sleep(2)
            delete_lines(1)
            credentials = True
        else:
            delete_lines(3)
            print(f'{bcolors.fail}The two passwords have to match{bcolors.endc}')

def load_credentials(): # loads existing credentials
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as file:
            pws = file.read()
            return json.loads(pws)

def ask_credentials():
    credentials = load_credentials()
    credentials.pop(0)
    if len(credentials) > 0:
        for i in range(len(credentials)):
            del credentials[i][-1:]
            credentials[i][1] = decrypt_data(key, credentials[i][1])
            credentials[i][2] = decrypt_data(key, credentials[i][2])
        table = tabulate(credentials, headers=['ID', 'Service', 'Username', ], tablefmt='orgtbl')
        id = len(credentials) + 1
        while id < 1 or id > len(credentials):
            print(f'{table}\n')
            id = int(input('Enter the ID of the website: '))
            delete_lines(len(credentials) + 5)
            if id < 1 or id > len(credentials):
                print(f'{bcolors.warning}Please insert a valid ID{bcolors.endc}')
        return id
    else:
        delete_lines(1)
        print(f'{bcolors.warning}There are no stored credentials{bcolors.endc}')
        return 0

def modify_credentials(key, id, name, username, pw): # lets the user change already stored credentials
    credentials = load_credentials()
    credentials[id][1], credentials[id][2], credentials[id][3] = encrypt_data(key, name), encrypt_data(key, username), encrypt_data(key, pw)
    with open(credentials_file, 'w') as file:
        json.dump(credentials, file, indent = 4)

def decrypt_data(key_bytes: str, ciphertext_str: str) -> str:  # Makes the credentials readable and usable
    # print(f'{bcolors.okcyan}Decripting started{bcolors.endc}') # debug text
    # print(f'{bcolors.warning}Debug decrypt_data(1):\tiv:\t\t\t{iv}{bcolors.endc}') # debug text
    # print(f'{bcolors.warning}Debug decrypt_data(2):\tpadded key_bytes:\t{key_bytes}{bcolors.endc}') # debug text
    ciphertext_bytes = b64decode(ciphertext_str)
    # print(f'{bcolors.warning}Debug decrypt_data(3):\tciphertext_bytes:\t{ciphertext_bytes}{bcolors.endc}') # debug text
    # padded_ciphertext_bytes = pad(ciphertext_bytes, AES.block_size)
    # print(f'Debug decrypt_data(7):\tpadded ciphertext_bytes:\t{padded_ciphertext_bytes}') # debug text
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv)
    plaintext_bytes = cipher.decrypt(ciphertext_bytes)
    # print(f'{bcolors.warning}Debug decrypt_data(4)\tplaintext_bytes:\t{plaintext_bytes}{bcolors.endc}') # debug text
    unpadded_plaintext_bytes = unpad(plaintext_bytes, AES.block_size)
    # print(f'{bcolors.warning}Debug decrypt_data(5)\tunpadded_plaintext_bytes:\t{unpadded_plaintext_bytes}{bcolors.endc}') # debug text
    # print(f'{bcolors.okcyan}Decripting done{bcolors.endc}{bcolors.endc}') # debug text
    return unpadded_plaintext_bytes.decode('utf-8')

def login(): # asks for the main password to access the pw database
    pws = load_credentials()
    locked = True
    while locked:
        key = input(f'Insert your main password: {bcolors.blink}¶{bcolors.endc}')
        with open(credentials_file, 'r') as file:
            pw_check = pws[0][3]
        if sha256(key) == pw_check:
            delete_lines(2)
            locked = False
            print(f'')
        else:
            delete_lines(2)
            print(f'{bcolors.fail}Incorrect password, try again{bcolors.endc}')
    key_bytes = pad(key.encode('utf-8'), AES.block_size)
    return key_bytes

def delete_lines(num_lines): # deletes lines, only function I made with chatGPT
    for i in range(num_lines):
        # Move cursor up one line
        print(f"\033[F", end='')
        # Clear the line
        print(f"\033[K", end='')

if __name__ == '__main__':
    # title
    print(f'{bcolors.header}██████╗ ██╗████████╗██╗    ██╗ █████╗ ██████╗ ██████╗ ███████╗███╗   ██╗     █████╗ ████████╗    ██╗  ██╗ ██████╗ ███╗   ███╗███████╗')
    print(f'██╔══██╗██║╚══██╔══╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝████╗  ██║    ██╔══██╗╚══██╔══╝    ██║  ██║██╔═══██╗████╗ ████║██╔════╝')
    print(f'██████╔╝██║   ██║   ██║ █╗ ██║███████║██████╔╝██║  ██║█████╗  ██╔██╗ ██║    ███████║   ██║       ███████║██║   ██║██╔████╔██║█████╗  ')
    print(f'██╔══██╗██║   ██║   ██║███╗██║██╔══██║██╔══██╗██║  ██║██╔══╝  ██║╚██╗██║    ██╔══██║   ██║       ██╔══██║██║   ██║██║╚██╔╝██║██╔══╝  ')
    print(f'██████╔╝██║   ██║   ╚███╔███╔╝██║  ██║██║  ██║██████╔╝███████╗██║ ╚████║    ██║  ██║   ██║       ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗')
    print(f'╚═════╝ ╚═╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝{bcolors.endc}\n\n')

    # signin screen
    if not os.path.exists(credentials_file):
        signin()

    # mandatory login screen
    key = login()

    # uncomment this section to test all the functionalities right after logging in the program (it should work tho)

    # test_plaintext = f'something'
    # print(f'{bcolors.warning}Debug main(1):\t\ttest:\t\t\t{test_plaintext}{bcolors.endc}') # debug text
    # byte_test = test_plaintext.encode('utf-8')
    # print(f'{bcolors.warning}Debug main(2):\t\tbyte_test:\t\t{byte_test}{bcolors.endc}') # debug text
    # padded_test = pad(byte_test, AES.block_size)  # Pad the key to the correct length
    # print(f'{bcolors.warning}Debug main(3):\t\tpadded_test:\t\t{padded_test}{bcolors.endc}') # debug text
    # print(f'{bcolors.warning}\t\t\tpadded_test_str:\t{bcolors.underline}{padded_test.decode('utf-8')}{bcolors.endc}') # debug text
    # encrypted_test= encrypt_data(key, test_plaintext)
    # print(f'{bcolors.warning}Debug main(4):\t\tencrypted test:\t\t{encrypted_test}{bcolors.endc}') # debug text
    # print(f'{bcolors.warning}Debug main(5):\t\tiv:\t\t\t{iv}') #debug text
    # decrypted_test = decrypt_data(key, encrypted_test)
    # print(f'{bcolors.warning}Debug main(6):\t\tdecrypted test:\t{decrypted_test}{bcolors.endc}') # debug text

    run = True
    while run:
        # main screen
        mode = None
        while mode != 1 and mode != 2 and mode != 3 and mode != 4 and mode != 5:
            print(f'Select an option: ')
            print(f'\t1. Search existing credentials')
            print(f'\t2. Add new credentials')
            print(f'\t3. Modify existing credentials')
            print(f'\t4. Delete existing credentials')
            print(f'\t5. Quit the program')
            mode = int(input('Select: '))
            if mode != 1 and mode != 2 and mode != 3 and mode != 4 and mode != 5:
                delete_lines(8)
                print(f'{bcolors.warning}Please insert a valid number{bcolors.endc}')
        delete_lines(7)

        if mode == 5:
            print(f'')
            terminate = 0
            while terminate == 0:
                terminate = input('Are you sure you want to quit the program? (y/n) ')
                if terminate == 'y':
                    run = False
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif terminate == 'n':
                    delete_lines(2)
                else:
                    delete_lines(2)
                    print(f'{bcolors.warning}Please enter y or n{bcolors.endc}')
                    terminate = 0

        elif mode == 1:
            id = ask_credentials()
            if id != 0:
                credentials = load_credentials()
                service_credential = []
                service_credential.append(credentials[id])

                for i in range(1,4):
                    service_credential[0][i] = decrypt_data(key, service_credential[0][i])

                print(f'\n{tabulate(service_credential, headers=['ID', 'Service', 'Username', 'Password'], tablefmt='orgtbl')}\n')
                input(f'{bcolors.waitingInput}Press enter to go back to the main menu{bcolors.endc}')
                delete_lines(5)

        elif mode == 2:
            delete_lines(1)
            name = input('\nInsert the name of the service: ')
            username = input('Insert your username/email/phone number: ')
            pw = input('Insert your password: ')
            save_credentials(key, name, username, pw)
            delete_lines(3)

        elif mode == 3:
            id = ask_credentials()
            if id != 0:
                credentials = load_credentials()

                name = input('Insert the name of the service: ')
                username = input('Insert your username/email/phone number: ')
                pw = input('Insert your password: ')
                modify_credentials(key, id, name, username, pw)
                delete_lines(3)

        elif mode == 4:
            id = ask_credentials()
            if id != 0:
                credentials = load_credentials()
                credentials.pop(id)
                with open(credentials_file, 'w') as file:
                    json.dump(credentials, file, indent=4)
                print(f'') # for some reason everytime the program runs this part of the code it will erase 1 extra line of console output, I'm too lay to find were I'm using the delete_lines() func a bit to much

        credentials = load_credentials()
        for id in range(0, len(credentials)):
            credentials[id][0] = id
        with open(credentials_file, 'w') as file:
            json.dump(credentials, file, indent = 4)

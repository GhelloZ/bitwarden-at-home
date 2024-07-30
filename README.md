# Bitwarden at Home

This console application is a simple password manager that allows users to securely store, retrieve, and manage their credentials. It uses AES encryption to protect the stored data and provides a console interface for interacting with the credentials.

## Table of Contents

- [Features](#features)
- [Main Execution](#main-execution)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Encryption Details](#encryption-details)
- [Code Analysis](#code-analysis)
- [Acknowledgments](#acknowledgments)

## Features

- Store and manage credentials securely using AES encryption.
- Retrieve and display stored credentials.
- Modify and delete existing credentials.
- User-friendly console interface with colored text for better readability.
- Secure login with a main password to access the credential database.

## Main Execution

- Displays a title screen.
- If the credentials file doesn't exist, it runs the `signin()` function.
- Prompts the user to log in with the main password.
- Provides a main menu to search, add, modify, or delete credentials, or to quit the program.

## Dependencies

The script requires the following Python packages:

- `json`: For handling JSON data.
- `tabulate`: For displaying data in a tabular format.
- `hashlib`: For SHA-256 hashing.
- `pycryptodome`: For AES encryption and decryption.

If any of these packages is missing, the program will automatically install them for you the frst time you run it

## Usage

1. **Initial Setup:**
   - The first time you run the script, it will prompt you to set a main password. This password is used to protect all your other credentials.

2. **Login:**
   - Each time you run the script after the initial setup, you will need to enter the main password to access the credential database.

3. **Main Menu:**
   - After logging in, you will be presented with the following options:
     1. Search existing credentials.
     2. Add new credentials.
     3. Modify existing credentials.
     4. Delete existing credentials.
     5. Quit the program.

4. **Managing Credentials:**
   - Follow the on-screen prompts to add, search, modify, or delete credentials. Credentials are stored in a JSON file with encryption.

## File Structure

- **credentials_file:** The JSON file used to store encrypted credentials. By default, the file name is `credentials.i_just_discovered_i_can_give_whatever_file_extension_i_want`.

## Encryption Details

- **AES Encryption:** The script uses AES encryption (CBC mode) to protect the credentials.
- **SHA-256 Hashing:** The main password is hashed using SHA-256 to verify user identity.

## Code Analysis

### Classes

#### `bcolors`
A class containing ANSI escape sequences for colored console output.

### Functions

#### `sha256(text)`
Hashes a given text using SHA-256 and returns the hexadecimal digest.

#### `save_credentials(key, name, username, pw)`
Saves new credentials to the database, encrypting the name of the service, username, and password.

#### `encrypt_data(key_bytes, plaintext)`
Encrypts plaintext using AES encryption with the given key bytes.

#### `signin()`
Prompts the user to set a main password during the initial setup and saves it to the credentials file.

#### `load_credentials()`
Loads and returns existing still encrypted credentials from the credentials file.

#### `ask_credentials()`
Displays stored credentials and prompts the user to select one for further actions.

#### `modify_credentials(key, id, name, username, pw)`
Modifies existing credentials in the database with new values.

#### `decrypt_data(key_bytes, ciphertext_str)`
Decrypts an encrypted string using AES decryption with the given key bytes.

#### `login()`
Prompts the user to enter the main password to access the credential database.

#### `delete_lines(num_lines)`
Utility function to delete a specified number of lines from the console output for a better experience.

## Acknowledgments

- Special thanks to [AKX on StackOverflow](https://stackoverflow.com/questions/78798132/how-do-i-decrypt-a-cyphertext-encrypted-with-aes-with-pycryptodome?noredirect=1#comment138928412_78798132) for assistance with the `encrypt_data()` and `decrypt_data()` functions.
- Color codes for console text are based on a solution from [StackOverflow](https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal).

If there's something wrong with this readme file [blame chatGPT](https://chatgpt.com/share/bf7680a3-7150-4888-8db4-f1ae7ac3ca68)

# INF360 - Programming in Python
# John Lee
# Final Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning / learned. They can store
information like song title, link to the song, tuning, and capo position in a JSON file.
You can create, read, update and delete the songs. 
'''

# TODO
# Implement logging

# Try catch block not needed for these modules since they're available with python
# Import needed to use os.path.exists
import os
import sys
# For logging
import logging
logging.basicConfig(filename='myProgramLog.txt', 
                    level=logging.DEBUG, 
                    format='%(asctime)s -  %(levelname)s -  %(message)s')

logging.debug('Program starting...')

# Local module imports. Using from X import Y here to avoid having to type module name.
# Try catch block needed here since they're local modules
try:
    # Utility functions (used in Song class too)
    from utils import *
    # Songs manager module (Manages CRUD operations for songs)
    from songs_manager import *
    logging.debug('Successfully imported local modules in main file.')
except:
    logging.critical('failed to import utils or songs_manager in main file')
    print('Failed to import utils or songs_manager in main file. Exiting.')
    sys.exit()

# File name to pass to functions. Should be in the same directory as the
# main file.
file = 'guitar_songs.json'

# Check if the file exists in current directory. If not, create it
if not os.path.exists(file):
    try:
        open(file, 'w+').close()
        logging.debug(f'Created file: {file}')
    except:
        # Print out error message before exiting. 
        logging.critical(f'Failed to create file: {file}')
        print('Could not create file. Exiting...')
        sys.exit()

# Prints menu
def print_menu():
    while True:
        print("""
*****************
    MAIN MENU   
*****************
""")
        print('1. Add new song')
        print('2. Search for a song')
        print('3. Show all songs')
        print('4. Quit')
        print()

        choice = get_valid_choice(1, 4)
        handle_menu_choice(choice)

# Handles the user input from the menu
# Decided to break it into two functions because the print_menu() felt too bloated
def handle_menu_choice(choice):
    match choice:
        case 1:
            add_new_song(file)
        case 2:
            song_obj = search_song(file)

            if song_obj:
                manage_song(file, song_obj) 
                return
            else:
                print('\nSong not found!\n')
        case 3:
            print_songs(file)
        case 4:
            print('\nGoodbye!')
            sys.exit()

    # Add pause after choosing menu options to allow user
    # to see result. Doesn't happen on choice 4 since
    # it exits without reaching this line.
    pause()

print_menu()
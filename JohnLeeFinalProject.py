# INF360 - Programming in Python
# John Lee
# Final Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning / learned. They can store
information like song title, link to the song, tuning, and capo position in a text file.
You can create, read, update and delete the songs. 
'''

# TODO
# Move get song info to song class
# Implement logging
# Sanitize input
# Multiple songs found in search_song()?

# Import needed to use os.path.exists
import os

# Local module imports. Using from X import Y here to avoid having to type module name
# Utility functions (used in Song class too)
from utils import *
# Songs manager module (Manages CRUD operations for songs)
from songs_manager import *

# File name to pass to functions. Should be in the same directory as the
# main file.
file = 'guitar_songs.json'

# Check if the file exists in current directory. If not, create it
if not os.path.exists(file):
    open(file, 'w+').close()

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
            exit()

    # Add pause after choosing menu options to allow user
    # to see result. Doesn't happen on choice 4 since
    # it exits without reaching this line.
    pause()

print_menu()
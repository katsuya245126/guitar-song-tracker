# INF360 - Programming in Python
# John Lee
# Midterm Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning / learned. They can store
information like song title, link to the song, tuning, and capo position in a text file.
'''

# TODO
# Add link opener
# make search_song() return dicitonary
# Implement get_all_songs()
# Use get_all_songs() in print_songs()
# Implement modify_song()
# Implement delete_song()
# Use regex in search to find parts
# Implement logging
# Sanitize input

# Import needed to use os.path.exists
import os
import re
import song

# File name to pass to functions. Should be in the same directory as the
# main file.
file = 'guitar_songs.txt'

# Check if the file exists in current directory. If not, create it
if not os.path.exists(file):
    open(file, 'w+').close()

# Gets song information and returns as a list
def get_song_info():
    title = input('Enter song title: ')
    link = input('Enter youtube link: ')
    tuning = input('Enter tuning: ')
    capo = input('Enter capo position: ')

    return [title, link, tuning, capo]

# Saves new song information in the given file
def save_new_song(file, song_list):
    new_song = '\t'.join(song_list)
    
    # I initially just had file.write() but I had issues managing
    # file modes (w, a, r), so I switched to with open()
    # to make sure the file is closed automatically.
    with open(file, 'a') as file:
        file.write(new_song + '\n')
    
    print('\nSong saved successfully!\n')

# Prints all the songs in the given file
def print_songs(file):
    # Open in read mode since we're just printing
    with open(file, 'r') as file:
        for song in file:
            # Strip the new line at the end of the row first, then split by tabs
            song_list = song.strip().split('\t')
            title, link, tuning, capo = song_list

            # Print the title on the first line
            print(f'Title: {title}')
            print()

            # Print the rest of the details below the title with indent
            print(f'\tYouTube Link: {link}')
            print(f'\tTuning: {tuning}')
            print(f'\tCapo: {capo}')
            
            print()

# Searches for the given song title and prints it
def search_song(song_title, file):
    # Clean the song title, then make regex object to match song title. Ignore case
    song_title = song_title.strip()
    song_regex = re.compile(fr'{song_title}', re.IGNORECASE)

    # Open in read mode since we're just printing
    with open(file, 'r') as file:
        for song_line in file:
            # Strip the new line at the end of the row first, then split by tabs
            song_list = song_line.strip().split('\t')
            title, link, tuning, capo = song_list

            # Return the song as dictionary
            if song_regex.search(title):
                song_obj = song.Song(title, link, tuning, capo)

                return song_obj
    
    print('\nSong not found!\n')

# Just adds a pause in between actions so user can see the results
def pause():
    input('Press Enter to continue...\n')

# Prints menu
def print_menu():
    while True:
        print()
        print('1. Add new song')
        print('2. Search for a song')
        print('3. Show all songs')
        print('4. Quit')
        print()

        user_input = input('Enter your choice: ')

        # Check if user entered a digit. If not, display error
        if not user_input.isdigit():
            print('\nPlease enter a number.\n')
            pause()
            continue

        match int(user_input):
            case 1:
                song_info = get_song_info()
                save_new_song(file, song_info)
            case 2:
                song_title = input('Enter song title: ')
                search_song(song_title, file)
            case 3:
                print_songs(file)
            case 4:
                return
            case _: # Default case if user enters a number other than 1 - 4
                print('\nPlease choose a number between 1 - 4\n')
        
        # Add pause after choosing menu options to allow user
        # to see result. Doesn't happen on choice 4 since
        # it exits without reaching this line.
        pause()

print_menu()
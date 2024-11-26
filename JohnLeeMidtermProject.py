# INF360 - Programming in Python
# John Lee
# Midterm Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning / learned. They can store
information like song title, link to the song, tuning, and capo position in a text file.
'''

# TODO
# Change to JSON
# Add link opener
# Implement get_all_songs()
# Use get_all_songs() in print_songs()
# Implement modify_song()
# Implement delete_song()
# Implement logging
# Sanitize input
# Multiple songs found in search_song()?

# Import needed to use os.path.exists
import os
import re
import song # My class
import json

# File name to pass to functions. Should be in the same directory as the
# main file.
file = 'guitar_songs.json'

# Check if the file exists in current directory. If not, create it
if not os.path.exists(file):
    open(file, 'w+').close()

# Reads all the data from the file and returns as a list of dictionary of songs
def get_all_songs(file):
    # Just in case there's an error with reading the json file
    try:
        # Open the file and load the content and return
        with open(file, 'r') as file:
            data = json.load(file)
        
        return data
    except:
        # It could return an error if the file is empty in which case we can just return empty list
        return []

# Gets song information and returns as a list
# ADD sanitizing!!!!!!!!!!!!
def get_song_info():
    title = input('Enter song title: ')
    link = input('Enter youtube link: ')
    tuning = input('Enter tuning: ')
    capo = input('Enter capo position: ')

    return song.Song(title, link, tuning, capo)

# Saves new song information in the given file
def save_new_song(file, song_obj):
    # Get list of all songs and append the new file
    songs_list = get_all_songs(file)
    songs_list.append(song_obj.dict())

    # Try saving song. Print messages accordingly
    try:
        # Overwrites the current file
        with open(file, 'w') as file:
            json.dump(songs_list, file, indent=4)
        
        print('\nSong saved successfully!\n')
    except:
        print('\nSomething went wrong!\n')

# Prints all the songs in the given file
def print_songs(file):
    songs_data = get_all_songs(file)

    for song_dict in songs_data:
        # values() returns the values as list, so we can unpack
        title, link, tuning, capo = song_dict.values()
        
        # Make Song object from the data and use the class' print() function
        # Making object for every song might seem inefficient but I don't think it matters at this scale
        song.Song(title, link, tuning, capo).print()

# Searches for the given song title and prints it
def search_song(song_title, file):
    # Clean the given song title, then make regex object to match song title. Ignores case
    song_title = song_title.strip()
    song_regex = re.compile(song_title, re.IGNORECASE)

    # Loop through all the songs 
    song_list = get_all_songs(file)
    for song_dict in song_list:
        # If song title matches the regex
        if song_regex.search(song_dict['title']):
            # Make Song object and return
            title, link, tuning, capo = song_dict.values()
            song_obj = song.Song(title, link, tuning, capo)

            return song_obj
    
    # If no matching title is found return None
    return None

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
                song_obj = search_song(song_title, file)
                if song_obj:
                    print()
                    song_obj.print()
                else:
                    print('\nSong not found!\n')
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
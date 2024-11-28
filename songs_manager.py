# INF360 - Programming in Python
# John Lee
# Final Project

# This module manages songs stored in a JSON file. It can read, print, add, search, edit, and delete songs.
# It uses the Song class to handle individual song details. 

# For handling json
import json
# Regex
import re

# Local module imports. Using from X import Y here to avoid having to type module name

# My class
from song import *
# Utility functions (used in Song class too)
from utils import get_valid_choice, pause

# Reads all the data from the file and returns as a list of dictionary of songs
def get_all_songs(file):
    # Just in case there's an error with reading the json file
    try:
        # Open the file and load the content and return
        with open(file, 'r') as file:
            data = json.load(file)
        
        return data
    except:
        # If the file is empty or we encounter
        # an error while reading file, we can just return empty list
        return []

# Prints all the songs in the given file
def print_songs(file):
    songs_data = get_all_songs(file)

    for song_dict in songs_data:
        # values() returns the values as list, so we can unpack
        title, link, tuning, capo = song_dict.values()

        # Make Song object from the data and use the class' print() function
        # Making object for every song might seem inefficient but I don't think it matters at this scale
        Song(title, link, tuning, capo).print()

# Gets song information and returns as a list
def get_song_info():
    new_song = Song()
    new_song.set_title()
    new_song.set_link()
    new_song.set_tuning()
    new_song.set_capo()

    return new_song  

# Saves new song information in the given file
def add_new_song(file):
    # Collect the new song info
    song_obj = get_song_info()

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

# Searches for the given song title and prints it
def search_song(file):
    # Get the song title
    song_title = input('Enter song title: ')

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
            song_obj = Song(title, link, tuning, capo)

            return song_obj
    
    # If no matching title is found return None
    return None

# Saves new song information in the given file
def delete_song(file, song_obj):
    # Get list of all songs and append the new file
    songs_list = get_all_songs(file)

    try:
        # Try to remove the song by matchign the dictionary
        # It should be found since song_obj was made by search_song()
        songs_list.remove(song_obj.dict())

        # Overwrite with the song removed
        with open(file, 'w') as file:
            json.dump(songs_list, file, indent=4)
        
        print("\nSong deleted!\n")
    except:
        print("\nSomethign went wrong!\n")

# Manages single song options
def manage_song(file, song_obj):
    while True:
        print()
        song_obj.print()
        print()
        print('1. Open link')
        print('2. Edit song')
        print('3. Delete song')
        print('4. Back')
        print()

        choice = get_valid_choice(1, 4)

        match choice:
            case 1:
                song_obj.open_link()
            case 2:
                song_obj.edit()
            case 3:
                delete_song(file, song_obj)
                # Goes back to the menu after deleting since there is nothing to edit after
                # the song is removed
                pause()
                return
            case 4:
                return
# INF360 - Programming in Python
# John Lee
# Final Project

# This module manages songs stored in a JSON file. It can read, print, add, search, edit, and delete songs.
# It uses the Song class to handle individual song details. 

# For handling json
import json
# Regex
import re
import logging
import sys

# Local module imports. Using from X import Y here to avoid having to type module name
try:
    # My class
    from song import *
    # Utility functions
    from utils import *
    logging.info('Successfully imported local modules in songs_manager.py')
except:
    logging.critical('Failed to import utils or song in songs_manager.py')
    print('Failed to import song or utils in songs_manager.py. Exiting...')
    sys.exit()

# Reads all the data from the file and returns as a list of dictionary of songs
def get_all_songs(file):
    # Just in case there's an error with reading the json file
    try:
        # Open the file and load the content and return
        with open(file, 'r') as file:
            data = json.load(file)
            logging.info(f'Successfully read all song data from {file.name}')
        
        # Return list of ditionary of songs
        return data
    except:
        # If the file is empty or we encounter
        # an error while reading file, we can just return empty list
        logging.error(f'Something went wrong reading file: {file.name} or the list is empty.')
        return []

# Prints all the songs in the given file
def print_songs(file):
    songs_data = get_all_songs(file)

    # If get_all_songs() returns an empty list, the file could be missing or empty
    if not songs_data:
        logging.warning(f'No songs found in {file}. File might be empty.')
        print('\nTHE LIST IS EMPTY!\n')
    else:
        logging.debug(f'Printing {len(songs_data)} songs from file.')
        for song_dict in songs_data:
            # values() returns the values as list, so we can unpack
            title, link, tuning, capo = song_dict.values()

            # Make Song object from the data and use the class' print() function
            # Making object for every song might seem inefficient but I don't think it matters at this scale
            Song(title, link, tuning, capo).print()

# Gets song information and returns the song object
def get_song_info():
    # Create song object and call each setter method to set the attributes
    # Inputs are sanitized within the method
    new_song = Song()
    new_song.set_title()
    new_song.set_link()
    new_song.set_tuning()
    new_song.set_capo()
    logging.debug(f'New song collected: {new_song.dict()}')

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
            logging.info(f'Added new song to {file.name}: {song_obj.dict()}')
        
        print('\nSong saved successfully!\n')
    except:
        logging.error(f'Something went wrong trying to add new song to {file.name}')
        print('\nSomething went wrong! Song not added.\n')

# Searches for the given song title and returns the song object
def search_song(file):
    # Get the song title
    song_title = input('Enter song title: ')

    # Clean the given song title, then make regex object to match song title. Ignores case
    song_title = song_title.strip()
    # Had to add re.escape() since special characters caused error
    song_regex = re.compile(re.escape(song_title), re.IGNORECASE)
    logging.info(f'Searching for song: {song_title}')

    # Loop through all the songs 
    song_list = get_all_songs(file)
    for song_dict in song_list:
        # If song title matches the regex
        if song_regex.search(song_dict['title']):
            logging.info(f'Matching song found: {song_dict}')
            # Unpack the tuples returned from values() to each variable
            title, link, tuning, capo = song_dict.values()
            # Make song object from the variables and return
            song_obj = Song(title, link, tuning, capo)

            return song_obj
    
    logging.info(f'No song matching {song_title} found.')
    # If no matching title is found return None
    return None

# Makes changes to the song and saves it
def edit_song(file, song_obj):
    # Get list of all songs
    songs_list = get_all_songs(file)

    # Using enumearte here since we need the index to replace the edited song
    for index, song_dict in enumerate(songs_list):
        # Compare dictionary
        if song_dict == song_obj.dict():
            logging.info(f'Editing song: {song_dict['title']}')
            # Make changes to the song_obj and replace the matching song in the list
            song_obj.edit()
            songs_list[index] = song_obj.dict()
            break
    
    # Save the songs list with the edited song
    try:
        with open(file, 'w') as file:
            json.dump(songs_list, file, indent=4)
            logging.info(f'Successfully saved edited song: {song_obj.dict()}')

        print('\nSong updated successfully!')
    except:
        logging.error(f'Somethign went wrong trying to edit song: {song_obj.dict()}')
        print('\nSomething went wrong! Song not edited.\n')

# Saves new song information in the given file
def delete_song(file, song_obj):
    # Get list of all songs
    songs_list = get_all_songs(file)

    try:
        # Try to remove the song by matchign the dictionary
        # It should be found since song_obj was made by search_song()
        # No need to use enumerate here since we are just removing the song and don't need the index
        songs_list.remove(song_obj.dict())

        # Overwrite with the song removed
        with open(file, 'w') as file:
            json.dump(songs_list, file, indent=4)
            logging.info(f'Successfully deleted song: {song_obj.dict()}')
        
        print("\nSong deleted!\n")
    except:
        logging.error(f'Something went wrong trying to delete song: {song_obj.dict()}')
        print("\nSomething went wrong! Song not deleted.\n")

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
                edit_song(file, song_obj)
            case 3:
                delete_song(file, song_obj)
                # Goes back to the menu after deleting since there is nothing to edit after
                # the song is removed
                pause()
                return
            case 4:
                return
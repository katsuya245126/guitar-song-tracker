# INF360 - Programming in Python
# John Lee
# Midterm Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning. They can store
information like song title, youtube link, tuning, and capo position.
'''

file = 'guitar_songs.txt'

def get_song_info():
    title = input("Enter song title: ")
    link = input("Enter youtube link: ")
    tuning = input("Enter tuning: ")
    capo = input("Enter capo position: ")

    return [title, link, tuning, capo]

def save_new_song(file, song_list):
    new_song = '\t'.join(song_list)
    
    # I initially just had file.write() but I had issues managing
    # file modes (w, a, r), so I switched to with open()
    # to make sure the file is closed automatically.
    with open(file, 'a') as file:
        file.write(new_song + '\n')

def print_songs(file):
    # Open in read mode since we're just printing
    with open(file, 'r') as file:
        for song in file:
            # Strip the new line at the end of the row first, then split by tabs
            song_list = song.strip().split('\t')
            title, link, tuning, capo = song_list

            # Print the title on the first line
            print(f"Title: {title}")
            
            # Print the rest of the details below the title with indent
            print(f"\tYouTube Link: {link}")
            print(f"\tTuning: {tuning}")
            print(f"\tCapo: {capo}")
            
            print()

def print_menu():
    return

print_songs(file)
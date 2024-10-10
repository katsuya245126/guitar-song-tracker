# INF360 - Programming in Python
# John Lee
# Midterm Project

'''
Guitar song tracker program

This program helps users keep track of songs they're learning / learned. They can store
information like song title, youtube link, tuning, and capo position in a text file.
'''

# File name to pass to functions. Should be in the same directory as the
# main file
file = 'guitar_songs.txt'

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
            
            # Print the rest of the details below the title with indent
            print(f'\tYouTube Link: {link}')
            print(f'\tTuning: {tuning}')
            print(f'\tCapo: {capo}')
            
            print()

# Searches for the given song title and prints it
def search_song(song_title, file):
    # Clean the song title and make it lower case
    song_title = song_title.strip().lower()

    # Open in read mode since we're just printing
    with open(file, 'r') as file:
        for song in file:
            # Strip the new line at the end of the row first, then split by tabs
            song_list = song.strip().split('\t')
            title, link, tuning, capo = song_list

            if title.lower() == song_title:
                # Print the title on the first line
                print(f'Title: {title}')
                
                # Print the rest of the details below the title with indent
                print(f'\tYouTube Link: {link}')
                print(f'\tTuning: {tuning}')
                print(f'\tCapo: {capo}')
                
                print()

                return
    
    print('\nSong not found!\n')

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


print_menu()
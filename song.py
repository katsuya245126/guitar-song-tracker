# INF360 - Programming in Python
# John Lee
# Final Project

# This class represents a song. It can print details about itself, open links, and edit attributes.
# It can also return itself as a dictionary.

# Module used to open links
import webbrowser
import logging
import sys

# Local module imports
try:
    # Utility functions
    from utils import *
    logging.info('Successfully imported local modules in song.py.')
except:
    logging.critical('Failed to import utils in song.py')
    print('Failed to import utils in song.py. Exiting...')
    sys.exit()

class Song:
    # Create new song with title, link, tuning, and capo
    def __init__(self, title="", link="", tuning="", capo=""):
        # Attributes default to empty string
        self.title = title
        self.link = link
        self.tuning = tuning
        self.capo = capo
    
    # Prints formatted values
    def print(self):
        # Print the title on the first line
        print(f'{self.title}')
        print()

        # Print the rest of the details below the title with indent
        print(f'\tLink: {self.link}')
        print(f'\tTuning: {self.tuning}')
        print(f'\tCapo: {self.capo}')
        
        print()
    
    # Opens the link of the song
    def open_link(self):
        logging.debug(f'Opening the link for {self.title}: {self.link}')
        webbrowser.open(self.link)

    # Sets the title of the song. Validates input. Accepts alphanumeric characters + space
    def set_title(self):
        while True:
            title = input('Enter title: ')
        
            # Have to remove spaces temporarily otherwise isalnum() returns false
            if title.replace(' ', '').isalnum():
                # If the new title is different from current one, log it
                # Using double quotes to surround the values in single quotes since if it's empty it might be hard to see in the log
                if title != self.title:
                    logging.info(f"Changing title from '{self.title}' to '{title}'")

                print(f'\nChanged title from {self.title} to {title}')
                self.title = title
                return
            else:
                print("\nInvalid title. Please only use alphanumeric characters + space\nPlease try again\n")
    
    # Sets the link of the song. Validates input
    def set_link(self):
        while True:
            link = input('Enter link: ')
        
            # Link has to start with 'http://' or 'https://' otherwise the webbrowser module
            # does not open the link. Also links should not contain spaces
            if link.startswith(('http://', 'https://')) and (not ' ' in link):
                # If the new link is different from current one, log it
                if link != self.link:
                    logging.info(f"Changing link from '{self.link}' to '{link}'")
                
                print(f'\nChanged link from {self.link} to {link}')
                self.link = link
                return
            else:
                print("\nLink cannot contain spaces and have to start with http:// or https://\nPlease try again\n")
    
    # Sets the tuning of the song. Validates input. 
    def set_tuning(self):
        while True:
            tuning = input('Enter tuning: ')
        
            # Only accepts alphabetic characters.
            if tuning.isalpha():
                # If the new tuning is different from current one, log it
                if tuning != self.tuning:
                    logging.info(f"Changing tuning from '{self.tuning}' to '{tuning}'")
                
                print(f'\nChanged tuning from {self.tuning} to {tuning}')
                self.tuning = tuning
                return
            else:
                print("\nInvalid tuning. Please only input alphabetic characters.\nPlease try again\n")

    # Sets the capo position of the song. Validates input. 
    def set_capo(self):
        while True:
            capo = input('Enter capo position: ')
        
            # Capo position should be a number and it should be between 0 (no capo) to 9.
            # Could maybe be higher but highly unlikely
            # Have to convert to int when comparing since it's still a string
            if capo.isdigit() and (int(capo) >= 0 and int(capo) <= 9):
                # If the new capo position is different from current one, log it
                if capo != self.capo:
                    logging.info(f"Changing capo position from '{self.capo}' to '{capo}'")
                
                print(f'\nChanged capo position from {self.capo} to {capo}')
                self.capo = int(capo)
                return
            else:
                print("\nInvalid capo position. Please choose a number between 0-9.\nPlease try again\n")
    
    # Edit menu handler
    def edit(self):
        while True:
            print()
            print("Edit Song:")
            print("1. Title")
            print("2. Link")
            print("3. Tuning")
            print("4. Capo")
            print("5. Back")
            print()

            choice = get_valid_choice(1, 5)

            match choice:
                case 1:
                    self.set_title()
                case 2:
                    self.set_link()
                case 3:
                    self.set_tuning()
                case 4:
                    self.set_capo()
                case 5:
                    break
        
    # Returns the object in dictionary form
    # Makes it easier to save to JSON
    def dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'tuning': self.tuning,
            'capo': self.capo
        }

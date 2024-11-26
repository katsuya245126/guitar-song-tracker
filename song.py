# To open links
import webbrowser
from utils import get_valid_choice

class Song:
    def __init__(self, title, link, tuning, capo):
        # Create new song with title, link, tuning, and capo
        # Assuming input is sanitized
        self.title = title
        self.link = link
        self.tuning = tuning
        self.capo = capo
    
    # Prints values
    def print(self):
        # Print the title on the first line
        print(f'{self.title}')
        print()

        # Print the rest of the details below the title with indent
        print(f'\tYouTube Link: {self.link}')
        print(f'\tTuning: {self.tuning}')
        print(f'\tCapo: {self.capo}')
        
        print()
    
    def open_link(self):
        webbrowser.open(self.link)

    # Edits the song info
    def edit(self):
        while True:
            print()
            print("Edit Song:")
            print("1. Title")
            print("2. YouTube Link")
            print("3. Tuning")
            print("4. Capo")
            print("5. Back")
            print()

            choice = get_valid_choice(1, 5)

            match choice:
                case 1:
                    self.edit_title()
                case 2:
                    self.edit_link()
                case 3:
                    self.edit_tuning()
                case 4:
                    self.edit_capo()
                case 5:
                    break
    
    # Changes the title of the song
    def edit_title(self):
        new_title = input("Enter new title: ").strip()

        # Make sure the title is not empty
        if new_title:
            self.title = new_title
            print("Title updated!")
        else:
            print("Invalid title!")

    # Changes the link of the song
    def edit_link(self):
        new_link = input("Enter new link: ").strip()

        # Make sure the link is not empty
        if new_link:
            self.link = new_link
            print("Link updated!")
        else:
            print("Invalid link!")

    # Changes the tuning of the song
    def edit_tuning(self):
        new_tuning = input("Enter new tuning: ").strip()

        # Make sure the tuning is not empty
        if new_tuning:
            self.tuning = new_tuning
            print("Tuning updated!")
        else:
            print("Invalid tuning!")

    # Changes the capo position of the song
    def edit_capo(self):
        print("Choose capo position 0 - 9\n")

        # Validation is handled in get_valid_choice()
        new_capo = get_valid_choice(0, 9)
        self.capo = new_capo
        print("Capo position updated successfully!")
        
    # Returns the object in dictionary form
    # Makes it easier to save to JSON
    def dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'tuning': self.tuning,
            'capo': self.capo
        }

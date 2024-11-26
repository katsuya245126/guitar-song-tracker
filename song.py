class Song:
    def __init__(self, title, link, tuning, capo):
        # Create new song with title, link, tuning, and capo
        # Assuming input is sanitized
        self.title = title
        self.link = link
        self.tuning = tuning
        self.capo = capo
    
    def print(self):
        # Print the title on the first line
        print(f'Title: {self.title}')
        print()

        # Print the rest of the details below the title with indent
        print(f'\tYouTube Link: {self.link}')
        print(f'\tTuning: {self.tuning}')
        print(f'\tCapo: {self.capo}')
        
        print()
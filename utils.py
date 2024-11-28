# INF360 - Programming in Python
# John Lee
# Final Project

# This module just stores utility functions

# Makes user choose between min and max number
def get_valid_choice(min, max):
    while True:
        choice = input('Enter your choice: ')

        if not choice.isdigit():
            print('\nPlease enter a number.\n')
            continue
        elif int(choice) < min or int(choice) > max:
            print(f'\nPlease choose a number between {min} - {max}\n')
            continue

        return int(choice)   

# Just adds a pause in between actions so user can see the results
def pause():
    input('Press Enter to continue...\n')
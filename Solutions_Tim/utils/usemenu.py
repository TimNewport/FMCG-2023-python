"""
This is a module called menu.py which has a single functions called menu.

The menu function should take any number of strings items as input and add them to a list of valid menu options.
    Then the menu function asked the user to enter an option and if the users value exists then return the users choice.
    If it does not ask them again. exit if no input given

"""

def menu(*options):
    """Menu created by input

    Returns:
        string: users choice from input
    """
    valid_options = list(options)

    while True:
        user_choice = input(f"Enter an option ({', '.join(valid_options)}) or press enter to exit: ")

        if user_choice == '':
            exit()
        elif user_choice in valid_options:
            return user_choice
        else:
            print(f"Invalid option '{user_choice}', try again.")

def menu2(*options):
    """Menu created by input with prices

    Returns:
        string: users choice from input
    """
    menu_options = {}
    for item in options:
        menu_options.update(item)

    while True:
        user_choice = input("Please enter an option: ")
        if user_choice == "":
            break
        elif user_choice in menu_options:
            return menu_options[user_choice]
        else:
            print("Invalid choice, please try again.")

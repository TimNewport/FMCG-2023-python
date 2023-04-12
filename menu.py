def menu(*args):
    while True:
        s = input(f'Choose from {args}: ').strip()

        if s in args:  # if the user chose a legit option
            return s

        print('Bad choice! Try again...')

def menu(*args):
    s = input('Choose: ').strip()

    if s in args:  # if the user chose a legit option
        return s

    print('Bad choice! Try again...')
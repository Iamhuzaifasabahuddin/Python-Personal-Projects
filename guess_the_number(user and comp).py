import random

try:
    def guess_number_user(x):
        number = random.randrange(1, x)
        chances = 3
        attempt = 0
        print(f"You have {chances} chances to guess the number correctly")
        print(f"The number lies between 1 and {x}")
        for i in range(1,chances+1):
            inp = int(input("Enter your number: "))

            if inp > number:
                print("Your number is too high")
                attempt += 1
                print("Attempt number:", attempt)
            elif inp < number:
                print("Your number is too low")
                attempt += 1
                print("Attempt number:", attempt)
            else:
                print(f"Wohoo! You did it, The number was {number}")
                break
            if attempt == chances:
                print(f"Uh oh you couldnt guess the number correctly in {chances} chances")



except AssertionError:
    print("guess should be a number only")

guess_number_user(10)


def guess_number_comp(x):
    checker = ''
    minimum = 1
    maximum = x
    while checker != 'c':
        if minimum != maximum:
            number = random.randrange(minimum, maximum)
        else:
            number = minimum

        checker = str(input(f"is the guess {number} (H) High,(L) Low or (C)Correct: ")).lower()

        if checker == 'h':
            maximum = number - 1
        elif checker == 'l':
            minimum = number + 1
    print("YOU GOT IT ")


guess_number_comp(100)
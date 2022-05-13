import random
import string
from assets.words import words


def get_valid_word(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = get_valid_word(words)
    word_letters = set(word)  # letters in the word
    alphabet = set(string.ascii_uppercase)  # letters in the english dictionary
    used_letters = set()  # what the user has guesssed

    lives = 6  # hardcoded

    # basically:
    # - get a random word
    # - store the letters in a set
    # - remove a letter from set when user guesses correctly
    # - or take a life if wrong guess
    while len(word_letters) > 0 and lives > 0:
        # show letters used
        if len(used_letters) > 0:
            print('\nYou have', lives, 'lives left and you have used these letters: ', ' '.join(
                used_letters))

        # show progress
        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))

        # get user input
        guess = input('\nGuess a letter: ').upper()
        if guess in alphabet - used_letters:
            # if not guessed before, store the guess
            used_letters.add(guess)

            # if correct guess
            if (guess in word_letters):
                word_letters.remove(guess)

            # take a life if wrong
            else:
                lives = lives - 1
                print(f'Letter {guess} is not in word.')

        elif guess in used_letters:
            print(
                f'You have already used character {guess}. Please try again.')

        else:
            print(f'Invalid character {guess}. Please try again.')

    # gets here when len(word_letters) == 0 or when lives == 0
    if lives == 0:
        print('You died, sorry.')
    else:
        # correct
        print(f'🎊 Yay, you guessed the word {word} correctly!!')

    # anyway show correct word
    word_list = [letter for letter in word]
    print('Correct word: ', ' '.join(word_list))


hangman()

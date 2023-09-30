import random
from words import words
import string

def get_valid_word():
    rand_word=random.choice(words)
    while '-' in rand_word or ' ' in rand_word:
        rand_word=random.choice(words)
    return rand_word.upper()

def hangman():
    print("\nGame Started...\n")
    rand_word=get_valid_word()
    word_letters=set(rand_word)
    used_letter=set()
    alphabet=set(string.ascii_uppercase)

    lives=6

    while len(word_letters)>0 and lives>0:
        print('\n*********************************************\nYou have ',lives,' lives left and you used letters: ', ','.join(used_letter))
        
        posi_in_word=[letter if letter in used_letter else '_' for letter in rand_word]
        print("Current Word: ", ' '.join(posi_in_word))

        user_letter=input("\nGuess a Letter : ").upper()
        if(user_letter in alphabet-used_letter):
            used_letter.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives=lives-1
                print("Letter not in the word.")
        elif user_letter in used_letter:
            print("You already use that letter.. Try Again")
        else:
            print("Invalid Character, Try b/w A~Z.")
    
    if(len(word_letters)==0):
        print("You Guessed The word!")
        posi_in_word=[letter if letter in used_letter else '_' for letter in rand_word]
        print("Word: ", ' '.join(posi_in_word))
    else:
        print("You died, Sorry...")
        print(f"The Word was {rand_word} !")

hangman()

print("\nGame Ended...\n")
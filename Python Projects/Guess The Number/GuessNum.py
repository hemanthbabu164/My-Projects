import random

def guess(x):
    random_number=random.randint(1,x)
    print("Guess The Number")
    while(True):
        choice=int(input(f"\nGuess the Number between 1 and {x} :"))
        if(choice==random_number):
            print("Your Choice is Correct!!!Congrats")
            break
        elif(choice<random_number):
            print("Your guess is lower, Guess HIGHER!!!")
        else:
            print("You crossed It!!, Guess lower")

def compGuess(x):
    low=1
    high=x
    isCorrect=''
    while isCorrect!='C':
        random_number=random.randint(low,high)
        isCorrect=input(f"\nIs {random_number} too High (H) ot too Low (L) or correct(C)\t:  ")
        if(isCorrect=='H'):
            high=random_number-1
        elif isCorrect=='L':
            low=random_number+1
    print("\nYay I Guessed your Number. :)")

def main():
    print("GAME STARTED......")
    while(True):
        choice=int(input("Press 1 if you want to Guess or anything else if you want Computer to Guess....:"))
        if(choice==1):
            range_x=int(input("\nChoose the range : "))
            guess(range_x)
        else:
            range_x=int(input("\nEnter the Range in which your number is : "))
            compGuess(range_x)
        ch=int(input("\nPress 0 to Exit, Anything Else to continue: "))
        if(ch==0):
            break
    print("\nGame Exited....")

if __name__=="__main__":
    main()
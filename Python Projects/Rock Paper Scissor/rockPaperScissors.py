import random

def play():
    user_choice=input("Whats your Choice? 'r' for rock, 'p' for papers, 's' for scissors\n")
    comp_choice=random.choice(['r','p','s'])
    if(user_choice==comp_choice):
        return "Its a Tie\n"
    if(is_win(user_choice,comp_choice)):
        return "You Won :)\n"
    return "You Lost :(\n"

def is_win(player,opponent):
    if (player=='r' and opponent=='s') or (player=='p' and opponent=='r') or (player=='s' and opponent=='p'):
        return True
    return False
    
print(play())
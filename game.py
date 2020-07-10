import random
SONGS=[["song author 1","song name 1"],["songauthor2","SONG2"],["Authorofsong3","Song Number 3"],["songAuthor4","song Number4"],["song author 1","another song"]]

def getfirstletters(phrase):
    shouldbeshown=True
    returnedphrase=""
    for letter in phrase:
        if letter==" ":
            returnedphrase+=(" ")
            shouldbeshown=True
        elif shouldbeshown:
            returnedphrase+=(letter)
            shouldbeshown=False
        else:
            returnedphrase+=("*")
    return returnedphrase


def playgame():
    global wrong_guesses
    wrong_guesses=0
    score=0
    while wrong_guesses<2:
        wrong_guesses = 0
        songselected=random.randrange(0,len(SONGS))
        songauthor=SONGS[songselected][0]
        songname=SONGS[songselected][1]
        namehidden = getfirstletters(songname)
        print("Author: "+songauthor)
        print("Name: "+namehidden)
        answeredcorrectly=guess_song(songname)
        if answeredcorrectly:
            score+=3
        else:
            answeredcorrectly = guess_song(songname)
            if answeredcorrectly:
                score+=1
    print("you scored:",score)




def guess_song(songname):
    global wrong_guesses
    guess = input("What is the name of the song?")
    if guess.upper() == songname.upper():
        print("match")
        return True
    else:
        print("Wrong try again")
        wrong_guesses += 1
        return False




if __name__ == '__main__':
    playgame()
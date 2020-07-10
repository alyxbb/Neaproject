import random

SONGS = [["song author 1", "song name 1"], ["songauthor2", "SONG2"], ["Authorofsong3", "Song Number 3"],
         ["songAuthor4", "song Number4"], ["song author 1", "another song"]]  # some fake songs for testing


def get_first_letters(phrase):  # returns the phrase with only the first character in each sentence shown
    should_be_shown = True  # should the next character be shown
    returned_phrase = ""

    for letter in phrase:
        if letter == " ":
            returned_phrase += " "
            should_be_shown = True  # if there's a space the next character should be shown

        elif should_be_shown:
            returned_phrase += letter
            should_be_shown = False  # add the character

        else:
            returned_phrase += "-"  # put * in place of the character

    return returned_phrase


def play_game():  # main function, plays the game
    still_playing = True
    score = 0
    while still_playing:  # repeatedly plays game until you lose

        song_selected = random.randrange(0, len(SONGS))  # pick random song

        # get variables associated with that song
        song_author = SONGS[song_selected][0]
        song_name = SONGS[song_selected][1]
        name_hidden = get_first_letters(song_name)

        # display the author and initials of song
        print("Author: "+song_author)
        print("Name: "+name_hidden)

        # get the user to guess the song
        answered_correctly = guess_song(song_name)
        if answered_correctly:
            score += 3  # if they got it correct score 3 points
        else:
            answered_correctly = guess_song(song_name)  # if they got it wrong try again
            if answered_correctly:
                score += 1  # if they get it right on the second go they get 1 point
            else:
                still_playing = False  # if they get it wrong twice end the game

    print("you scored:", score)  # display score at end of game


def guess_song(song_name):
    guess = input("What is the name of the song?")

    if guess.upper() == song_name.upper():  # use upper so capitalisation does not matter,
        print("match")  # if correct say it
        return True

    else:
        print("Wrong try again")  # doesnt match so they got it wrong
        return False


if __name__ == '__main__':  # run the game if this file is run
    play_game()

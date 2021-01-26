import random
import sqlite3
import hashlib
from getpass import getpass
conn = sqlite3.connect('data.db')
c = conn.cursor()
def createtables():
  
    c.execute("CREATE TABLE if not exists songs(name TEXT NOT NULL PRIMARY KEY, artist TEXT)")
    #create a table of songs containing the names and artists of the songs
    c.execute("CREATE TABLE if not exists highscores(score INTEGER, user TEXT)")
    #create a table of highscores
    c.execute("CREATE TABLE if not exists users(username TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL,admin INTEGER)")
    #create a table of usernames and hashed passwords.
    c.execute("SELECT * FROM users")#get a list of all users
    if len(c.fetchall())==0:#if there are no users,create a user
        print("---------setup---------")
        print("admin account setup")
        while True:#repeatedly get username until a valid username is entered
            username=input("username:")

            if len(username)==0:#if they didnt provide a username print an error
                print("please input a username")
                continue
            else:
                break#if they did provide a username exit the loop
        while True:
            while True:
                #repeatedly get password until password is valid.
                password = getpass("password:")

                if len(password)==0:#if they didnt provide a password print an error
                    print("please input a password")
                    continue
                else:
                    break#if they did provide a password exit the loop
            passwordcheck = getpass("retype password:")
            if passwordcheck!=password:#if passwords dont match then try again
                print("passwords do not match, please try again")
                continue
            else:
                break
        hashedpass=hashlib.sha3_512(bytes(password,"utf-8")).hexdigest()#hash the password
        password="NOPE"#set the password to nope so hackers dont know what the password was.
        c.execute("INSERT INTO users values(?, ?,1)",(username,hashedpass))#create the admin user
        
    conn.commit()#save the database

SONGS = [["song author 1", "song name 1"], ["songauthor2", "SONG2"], ["Authorofsong3", "Song Number 3"],["songAuthor4", "song Number4"], ["song author 1", "another song"]]  # some fake songs for testing


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

def login():
    while True:
        print("----------login----------")
        while True:

            #get username and password
            username=input("username:")
            password=getpass("password:")

            #hash password
            hashedpass=hashlib.sha3_512(bytes(password,"utf-8")).hexdigest()
            password="NOPE"

            #check if the user exists
            c.execute("SELECT username,admin FROM users WHERE username=? and password=?",(username,hashedpass))

            #if the user exists stop asking for username, otherwise continue asking for login details
            if c.fetchone() is  None:
                continue
            else:
                break
        

            


if __name__ == '__main__':  # run the game if this file is run
    createtables()
    login()

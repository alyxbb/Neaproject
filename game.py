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
    c.execute("SELECT * FROM users WHERE admin=1")#get a list of all users
    if len(c.fetchall())==0:#if there are no users,create a user
        print("---------account creation---------")

            
        while True:#repeatedly get username until a valid username is entered
            username=input("username:")

            if len(username)==0:#if they didnt provide a username print an error
                print("please input a username")
                continue
            else:
                break#if they did provide a username exit the loop
        while True:
            password = getpwd()
            passwordcheck = getpwd("retype password:")
            if passwordcheck!=password:#if passwords dont match then try again
                print("passwords do not match, please try again")
                continue
            else:
                break
        c.execute("INSERT INTO users values(?, ?,1)",(username,password))#create the admin user
        
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

def chooseoption(maxi):
    while True:
        choice=input("please input a number(1-"+str(maxi)+")")#get an input

        #check if the input is valid
        try:
            choiceNo=int(choice)
        except ValueError:
            print("please input a number")
            continue
        else:
            if choiceNo>maxi:
                print("number must be less than",maxi)
                continue
            elif choiceNo<1:
                print("number must be greater than 0")
                continue
            else:
                return choiceNo


def accountmanager(username,admin):
    while True:
        print("----------------account manager--------------")
        print("1.change username")
        print("2.change password")
        print("3.delete account")
        if admin:
            print("4.remove admin perms")
            print("5.exit account manager")
            maxchoice=5
        else:  
            print("4.exit account manager")
            maxchoice=4
        
        choiceNo=chooseoption(maxchoice)
        if choiceNo==1:
            while True:
                passw=getpwd()
                c.execute("SELECT username FROM users WHERE username=? and password=?",(username,passw))
                user=c.fetchone()
                if user is None:
                    print("incorrect password")
                    continue
                else:
                    break
            while True:
                newusername=input("new username:")

                if len(newusername)==0:#if they didnt provide a username print an error
                    print("please input a username")
                    continue
                else:
                    break
            c.execute("UPDATE users SET username=? WHERE username=?",(newusername,username))
            conn.commit()
        elif choiceNo==2:
            while True:
                passw=getpwd("old password:")
                c.execute("SELECT username FROM users WHERE username=? and password=?",(username,passw))
                user=c.fetchone()
                if user is None:
                    print("incorrect password")
                    continue
                else:
                    break
            while True:
                newpass=getpwd("new password:")
                newpasscheck=getpwd("repeat new password:")

                if newpass!=newpasscheck:#if they didnt provide a username print an error
                    print("passwords do not match, please try again")
                    continue
                else:
                    break
            c.execute("UPDATE users SET username=? WHERE username=?",(newusername,username))
            conn.commit()
        elif choiceNo==3:
            while True:
                passw=getpwd("password:")
                c.execute("SELECT username FROM users WHERE username=? and password=?",(username,passw))
                if user is None:
                    print("incorrect password")
                    continue
                else:
                    break
                
            confirmation=input("please type",username,"to confirm account deletion")
            if confirmation==username:
                c.execute("DELETE FROM users WHERE username=?",(username))
                conn.commit()
                return False,username
            else:
                print("cancelling...")
        elif choiceNo==4 and not admin:
            return True, username
        elif choiceNo==4 and admin:
            while True:
                passw=getpwd("password:")
                c.execute("SELECT username FROM users WHERE username=? and password=?",(username,passw))
                if user is None:
                    print("incorrect password")
                    continue
                else:
                    break
            confirmation=input("please type",username,"to confirm you want to lose admin permissions. this cant be undone")
            if confirmation==username:
                c.execute("UPDATE users SET admin=0 WHERE username=?",(username))
                conn.commit()
                return False,username
            else:
                print("cancelling...")
        elif choiceNo==5 and admin:
            return True, username

        
def songmanager():
    while True:
        print("----------------song manager--------------")
        print("1.add song")
        print("2.edit song")
        print("3.delete song")
        print("4.exit song manager")
        choiceNo=chooseoption(4)
        if choiceNo==1:
            while True:
                print("-----song adder-----")
                while True:
                    name=input("song name:")
                    if len(name)==0:
                        print("please input a song name")
                        continue 
                    artists=input("song artist:")
                    if len(artists)==0:
                        print("please input an artist")
                        continue
                    else:
                        break
                c.execute("INSERT INTO songs values(?, ?)",(name,artists))
                conn.commit()
                while True:
                    cont=input("would you like to continue (Y/N)").upper()
                    if cont!="Y" and cont!="N":
                        print("please input y or N")
                        continue
                    else:
                        break
                if cont=="Y":
                    print("adding next song")
                    continue
                elif cont=="N":
                    break
        if choiceNo==2:
            c.execute("SELECT * FROM songs")
            songslist=c.fetchall()
            songcount=len(songslist)
            digits=len(str(songcount))
            songs,artists=zip(*songslist)
            longestsonglen=len(max(songs,key=len))
            longestartistlen=len(max(artists,key=len))
            digitsstr=str(digits)+"d"
            
            for count, song in enumerate(songslist):
                countstr=format(count+1, digitsstr)
                songspaces=longestsonglen-len(song[0])
                artistspaces=longestartistlen-len(song[1])
                line="| "+countstr+" | "+song[0]+" "*songspaces+" | "+song[1]+" |"
                print(line)
            choice=chooseoption(songcount)
            songselected=songslist[choice-1]
            while True:
                print(songselected[0])
                print("1.change name")
                print("2.change artist")
                print("3.back")
                choiceid=chooseoption(3)
                if choiceid==1:
                    while True:
                        newname=input("new name:")
                        if len(newname)==0:
                            print("invalid name")
                            continue
                        else:
                            break
                    c.execute("UPDATE songs SET name=? WHERE name=?",(newname,songselected[0]))
                    conn.commit()

                elif choiceid==2:
                    while True:
                        newartist=input("new artist name:")
                        if len(newname)==0:
                            print("invalid artist name")
                            continue
                        else:
                            break
                    c.execute("UPDATE songs SET artist=? WHERE name=?",(newartist,songselected[0]))
                    conn.commit()
                elif choiceid==3:
                    break



        if choiceNo==3:
            c.execute("SELECT * FROM songs")
            songslist=c.fetchall()
            songcount=len(songslist)
            digits=len(str(songcount))
            songs,artists=zip(*songslist)
            longestsonglen=len(max(songs,key=len))
            longestartistlen=len(max(artists,key=len))
            digitsstr=str(digits)+"d"
            
            for count, song in enumerate(songslist):
                countstr=format(count+1, digitsstr)
                songspaces=longestsonglen-len(song[0])
                artistspaces=longestartistlen-len(song[1])
                line="| "+countstr+" | "+song[0]+" "*songspaces+" | "+song[1]+" |"
                print(line)
            choice=chooseoption(songcount)
            confirm=input("are you sure you want to delete this song?(Y/N)").upper()
            songselected=songslist[choice-1][0]
            if confirm=="Y":
                c.execute("DELETE FROM songs WHERE name=?",songselected)
                conn.commit()
        elif choiceNo==4:
            return

def usermanager(username,admin):
    print("1.list users")
    print("2.add user")
    print("3.change a username")
    print("3.delete a user")
    print("4.quit")
    choiceid=chooseoption(6)
    if choiceid==1:
        c.execute("SELECT username, admin FROM users")
        userlist=c.fetchall()
        usercount=len(userlist)
        digits=len(str(usercount))
        users,admins=zip(*userlist)
        longestuserlen=len(max(users,key=len))
        digitsstr=str(digits)+"d"    
        for count, usern in enumerate(userlist):
            countstr=format(count+1, digitsstr)
            userspaces=longestuserlen-len(usern[0])
            if usern[1]==1:
                admintext="admin"
            else:
                admintext="     "
            line="| "+countstr+" | "+usern[0]+" "*userspaces+" | "+admintext+" |"
            print(line)

    elif choiceid==2:
        while True:
            adminresponse=input("should this user be an admin?(Y/N").upper()
            if adminresponse=="Y":
                newuserisadmin=1
                break
            elif adminresponse=="N":
                newuserisadmin=0
                break
            else:
                print("please input Y or N")
                continue
        print("---------account creation---------")
        print("you can now let the user do this. you will be automatically signed out")

            
        while True:#repeatedly get username until a valid username is entered
            username=input("username:")

            if len(username)==0:#if they didnt provide a username print an error
                print("please input a username")
                continue
            else:
                break#if they did provide a username exit the loop
        while True:
            password = getpwd()
            passwordcheck = getpwd("retype password:")
            if passwordcheck!=password:#if passwords dont match then try again
                print("passwords do not match, please try again")
                continue
            else:
                break
        c.execute("INSERT INTO users values(?, ?,?)",(username,password,newuserisadmin))#create the admin user
        conn.commit()
        return False


    elif choiceid==3:
        c.execute("SELECT username, admin FROM users")
        userlist=c.fetchall()
        usercount=len(userlist)
        digits=len(str(usercount))
        users,admins=zip(*userlist)
        longestuserlen=len(max(users,key=len))
        digitsstr=str(digits)+"d"    
        for count, usern in enumerate(userlist):
            countstr=format(count+1, digitsstr)
            userspaces=longestuserlen-len(usern[0])
            if usern[1]==1:
                admintext="admin"
            else:
                admintext="     "
            line="| "+countstr+" | "+usern[0]+" "*userspaces+" | "+admintext+" |"
            print(line)
        choice=chooseoption(usercount)
        userselected=userlist[choice-1]
        while True:
            newname=input("new name:")
            if len(newname)==0:
                print("invalid name")
                continue
            else:
                break
        c.execute("UPDATE users SET usernamename=? WHERE usernamename=?",(newname,userselected[0]))
        conn.commit()
    elif choiceid==4:
        c.execute("SELECT username, admin FROM users")
        userlist=c.fetchall()
        usercount=len(userlist)
        digits=len(str(usercount))
        users,admins=zip(*userlist)
        longestuserlen=len(max(users,key=len))
        digitsstr=str(digits)+"d"    
        for count, usern in enumerate(userlist):
            countstr=format(count+1, digitsstr)
            userspaces=longestuserlen-len(usern[0])
            if usern[1]==1:
                admintext="admin"
            else:
                admintext="     "
            line="| "+countstr+" | "+usern[0]+" "*userspaces+" | "+admintext+" |"
            print(line)
        choice=chooseoption(usercount)
        userselected=userlist[choice-1]
        confirm=input("are you sure you want to delete this user?(Y/N)").upper()
        if confirm=="Y":
                c.execute("DELETE FROM users WHERE username=?",userselected[0])
                conn.commit()
    elif choiceid==5:
        return True



def mainmenu(user):
    #set admin variable
    if user[1]==1:
        admin=True
    else:
        admin=False
    username=user[0]

    #print menu
    print("--------------menu----------------")
    print("1.logout")
    print("2.play")
    print("3.leaderboard")
    print("4.account managment")
    options=4
    #if they are an admin show the admin only options
    if admin:
        options=6
        print("5.song managment")
        print("6.user managment")
    choiceNo=chooseoption(options)

    if choiceNo==1:
        #reset user variables for increased security
        user=tuple()
        username=""
        admin=False
        return
    elif choiceNo==2:
        play_game()
    elif choiceNo==3:
        print("leaderboard not implemented")
        #need to add leaderboard functionality
    elif choiceNo==4:
        accountexists,newusername=accountmanager(username,admin)
        username=newusername
        if accountexists==False:
            user=tuple()
            username=""
            admin=False
            return
    elif choiceNo==5 and admin:
        songmanager()
    elif choiceNo==6 and admin:
        stayloggedin=usermanager(username,admin)
        if not stayloggedin:
            user=tuple()
            username=""
            admin=False
            return


def getpwd(message="password:"):
    while True:     
        password=getpass(message)
        if len(password)==0:#if they didnt provide a password print an error
            print("please input a password")
            continue
        else:
            hashedpass=hashlib.sha3_512(bytes(password,"utf-8")).hexdigest()
            password="NOPE"
            break
    
        #hash password
        
    return hashedpass
        


def login():
    while True:
        while True:
            print("----------login----------")
            

            #get username and password
            username=input("username:")
            hashedpass=getpwd()

            #check if the user exists
            c.execute("SELECT username,admin FROM users WHERE username=? and password=?",(username,hashedpass))
            user=c.fetchone()
            #if the user exists stop asking for username, otherwise continue asking for login details
            if user is  None:
                print("the username and password do not match")
                continue
            else:
                break
        mainmenu(user)
        
if __name__ == '__main__':  # run the game if this file is run
    createtables()
    login()

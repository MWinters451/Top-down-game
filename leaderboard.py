# import modules
import tkinter
import os

def FetchScores():
    HS_names = []
    HS_scores = []
    if os.path.exists("highscore.csv"): # if there is a file that exists
        file = open("highscore.csv", "r") # open the file as read
        read_file = file.read().split(",") # read it and split it at every ,
        final_list = []
        for i in read_file:
            final_list += i.split("\n") # split it where it would be a new line
        final_list.pop()
        counter = 0
        for i in final_list:
            counter+=1
            if counter%2 == 0:
                HS_scores.append(i) # seperate the list of the scores and names here 
            else:
                HS_names.append(i)
        file.close() # close the file
        return HS_names, HS_scores # return the list of names an scores
    else:
        #print("No file found") # if there is no file to open we just return an empty list
        return [], []

def SaveScore(NewName, NewScore):
    HS_names, HS_scores = FetchScores() # grab the current high scores
    if len(HS_scores)>0: # if there are scores that are currently saved
        for i in range(len(HS_scores)):
            if NewScore >= int(HS_scores[i]): # if they score is better than a current score 
                HS_names.insert(i, NewName)
                HS_scores.insert(i, NewScore)   # add the name and score to the lists
                break
            elif i == len(HS_scores)-1: # or if it is the last score
                HS_names.append(NewName)
                HS_scores.append(NewScore)  # add the name and score to the lists
                break
    else:
        # if there are no current scores then we can just add the scores to the list
        HS_names.append(NewName)
        HS_scores.append(NewScore) 
    toWrite = ""
    for i in range(len(HS_names)):
        # setting up the strin that we are going to write to the file
        toWrite = toWrite+ str(HS_names[i])+","+str(HS_scores[i])+"\n" 
    try:
        #print(toWrite)
        file = open("highscore.csv", "w") # we can open the file and write everything to it
        file.write(toWrite)
        file.close()
    except Exception as e:
        print(e)
            
class PopUp(tkinter.Toplevel):
    player_name = ""
    def __init__(self, master, score):
        tkinter.Toplevel.__init__(self, master)
        self.title("Game Over")
        self.text = "Game Over! Your score was: "+str(score)
        self.display_note_gui()

    def display_note_gui(self):
        self.geometry("300x150") # increase size of the window so it's not too small

        # lables to tell the player their score and what to do.
        tkinter.Label(self, text = self.text, font=("Arial", 12)).pack()
        tkinter.Label(self, text = "Enter your name below:", font=("Arial", 12)).pack()

        # this is the space for the player to input their name
        self.input_name = tkinter.Entry(self)
        self.input_name.pack()

        # button that will run the submit_name function when pressed
        tkinter.Button(self, height =2, width = 20, text='Confirm', command = self.sumbmit_name).pack()

    # this will set the player_name variable to the input name so that it can be accessed
    def sumbmit_name(self):

        # i do this to remove any spaces or special characters from the name so that it won't cause errors
        temp = "".join(c for c in self.input_name.get() if c.isalnum())

        if temp != "": # now we check if the name is valid once everything else is removed
            self.player_name = temp # we not set the name
            self.destroy() # we stop the window from showing as its not needed            
            
        

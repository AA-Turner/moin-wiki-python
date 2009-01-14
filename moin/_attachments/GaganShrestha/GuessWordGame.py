#Author : Gagan Shrestha
#Description : I am trying to recreate the Game that I had created long time back using C++ to win a programming contest

import random       #need to generate random no.

#Describing the rules to the players
print """Welcome to this home-made game. I call it "GuessTheWord" !
The game, as its name suggests, is to guess a word. You will see the blanks representing the letters in a word. So, cue no. 1 - You know the no. of letters in the word.

You need to enter one letter at a time as your guess. If the letter exists in the guess word, the blanks will be replaced for each occurrence of the entered letter.

Press Ctrl+c to quit the game.

Now lets start the game !!!"""         


print 50*'-'

#function to display list
def dispList(list):
    print "\n"
    for i in list:
        print i,
    print "\n"
    
#function to check the presence of character in the string
def ifPresent(char,str):
    return str.count(char)
        
#function to find the indices of the character in the list
def findIndex(char,str):
    i=0
    indexList=[]
    #print len(str)         for debugging
    while i < len(str):
        if char==str[i]:
            indexList.append(i)
        i=i+1
    return indexList    

#function to fill the characters in the list
def fillList(char,indexList,List):
    i=0
    for i in indexList:
        List[i]=char
    #print answerList       for debugging           
    return List    

#retrieve list of strings for questions from config file called 'questions.txt'
strings=[]          #this list will hold the words to be guessed from config file
file=open('questions.txt','r')
for string in file.readlines():
    strings.append(string.rstrip())
file.close()

#choose the string for question
random.shuffle(strings)
i=random.randint(0,(len(strings)-1))    

#variable to control the main loop of game
loop=1

#variable to check the count of try
count=0

#need to create list of blanks
repeat=len(strings[i])
fill=0

#This list is to create a question
question=[]

#This list is to store the user's guess
answer=[]

#this list will be used to record the player's guess
while fill < repeat:
    #let us fill the answer list with hyphens
    question.append(strings[i][fill].lower())
    answer.append('-')
    fill=fill+1

#dispList(question)         #for debugging
#display the empty list
print "\n\n"    
dispList(answer)

print ""
print ""

#Actual program starts here
while loop==1:

    if (answer == question):
        print '\nCongratulations ! You got it !! You took',count,'attempts to get the right answer !!!  \n'
        break

    #take the input from player
    try:
        char=raw_input("\nEnter your guess character: ").lower()
        count=count+1
        
    except(EOFError):
        print '\n\nCharacter you entered is not in the answer. Try again !'
        continue

    except(KeyboardInterrupt):
        print '\n\nYou chose to quit the game ! See you later !!!'
        break

    #check if player entered more than one character and display error if yes
    if len(char)>1:
        print '\nEnter only one character at a time !\n'
        dispList(answer)
        continue    
        
    #check if input is present in our answer
    elif ifPresent(char,strings[i]):
        #print 'Character present'      for debugging

        #since it is present call the function to find the index no. on which the entered character is present    
        indexList=findIndex(char,strings[i])

        #print indexList                for debugging

        #filling the character in the answer list wherever it is present based on index we found earlier
        answer=fillList(char,indexList,answer)

        #print answer                   for debugging

        #display the answer with input filled in
        dispList(answer)    

    #give another chance to player since character entered earlier is not present in our answer                        
    else:
        print '\nCharacter you entered is not in the answer. Try again !'
        dispList(answer)
        continue       

#print 'Out of Loop ! phew !!'          for debugging

#End of Programme



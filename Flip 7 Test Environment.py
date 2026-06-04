import random

#All cards:
#X of each X card (i.e 12 twelve cards) +10 Actions +6 Modifiers = 108 Cards
#There also 3 unique num cards: Lucky 13, Unlucky 7, The Zero
#2d array to store (name) and (how many?) and (how many left?)

gameCards = [["13",12,12], #Has unique among 13
             ["12",12,12],
             ["11",11,11],
             ["10",10,10],
             ["9",9,9],
             ["8",8,8],
             ["7",6,6], #Has unique among 7
             ["6",6,6],
             ["5",5,5],
             ["4",4,4],
             ["3",3,3],
             ["2",2,2],
             ["1",1,1],
             ["The 0",1,1], 
             ["Lucky 13",1,1],
             ["Unlucky 7",1,1]]
             #["Discard",2,2], #Removed for testing purposes, should be re-added for gameplay
             #["Flip 4",2,2],
             #["Swap",2,2],
             #["Just One More",2,2],
             #["Steal",2,2],
             #["-2",1,1],
             #["-4",1,1],
             #["-6",1,1],
             #["-8",1,1],
             #["-10",1,1],
             #["/2",1,1]] 

masterList = []
currentHand = []
heuristicsData = [] 
strategyData = []

choice = ""
score = 0
roundNum = 1
cumulativeProb = 1.0
count = 0

for i in range(0,len(gameCards)):
    for j in range(0,gameCards[i][1]):
        masterList.append(gameCards[i][0])

random.shuffle(masterList)

def FlipCard():
    global currentHand
    global masterList
    global gameCards
    global cumulativeProb
    if masterList[0] == "Unlucky 7":
        currentHand = ["Unlucky 7"]
        cumulativeProb = 1.0
        print("Bad Luck! Hand Reset due to Unlucky 7!")
    else:
        currentHand.append(masterList[0])
        for i in range(0,len(gameCards)):
            if masterList[0] == gameCards[i][0] :
                gameCards[i][2] -= 1
    masterList.remove(masterList[0])
    print("Your current hand is: " + str(currentHand))
   
def CheckFlip7():
    global currentHand
    tempHand = []
    for i in range(0,len(currentHand)):
        if currentHand[i].isnumeric() or currentHand[i] == "The 0" or currentHand[i] == "Unlucky 7" or currentHand[i] == "Lucky 13":
            tempHand.append(currentHand[i])
    if len(tempHand) == 7 :
        print("Flipped 7!")
        return True
   
def CheckBust():
    global currentHand
    tempHand = []
    for i in range(0,len(currentHand)):
        if currentHand[i] in tempHand or ((currentHand[i] == "7") and ("Unlucky 7" in tempHand)) or ((currentHand[i] == "Unlucky 7") and ("7" in tempHand)):
            print("You Busted!")
            return True
        else:
            tempHand.append(currentHand[i])

def CheckScore():
    global score
    print("Your current score is: " + str(score))

def CheckHand():
    global currentHand
    print("Your current hand is: " + str(currentHand))
            
def ResetHand():
    global currentHand
    currentHand = []
    print("")
    print("Round " + str(roundNum))
    
def ReshuffleDeck(pHand):
    global gameCards
    global masterList
    for i in range(0,len(gameCards)):
        gameCards[i][2] = gameCards[i][1]
        for j in range(0,gameCards[i][1]):
            masterList.append(gameCards[i][0])
    for i in range(0, len(pHand)):
        masterList.remove(pHand[i])
    random.shuffle(masterList)
    
def Bank(pBonus=0):
    global currentHand
    global score
    addToScore = 0 #needed for intereactions with the 0
    temp0Flag = False
    for i in range(0,len(currentHand)):
        if currentHand[i].isnumeric() :
            addToScore += int(currentHand[i])
        elif currentHand[i] == "Lucky 13":
            addToScore += 13
        elif currentHand[i] == "Unlucky 7":
            addToScore += 7
        elif currentHand[i] == "The 0":
            temp0Flag = True
    if temp0Flag :
        if pBonus == 0 :
            print("Banked Nothing!")
        else:
            score += addToScore
            score += pBonus
            print("You scored " + str(addToScore+pBonus)+" for this round!")
    else:
        score += addToScore
        score += pBonus
        print("You scored " + str(addToScore+pBonus)+" for this round!")
    print("Your total score is: " + str(score))
    
def ShowProbBust():
    global currentHand
    global gameCards
    totalCards = 0
    playerWeight = 0
    bustChance = 0.0 #Decimal Probability
    bustPerc = 0.0 #Percent Chance
    for i in range(0,len(gameCards)):
        totalCards += gameCards[i][2]
        for j in range(0,len(currentHand)):
            if currentHand[j] == gameCards[i][0]:
                playerWeight += gameCards[i][2]
                
    bustChance = playerWeight/totalCards
    bustProb = round((bustChance*100),3)
    
    #print("Your chances of busting are: " + str(bustProb) + "%")
    return(bustChance)

def CheckHandScore(pMode = 0):
    global currentHand
    
    addToScore = 0 #needed for intereactions with the 0
    temp0Flag = False
    total = 0
    for i in range(0,len(currentHand)):
        if currentHand[i].isnumeric() :
            addToScore += int(currentHand[i])
        elif currentHand[i] == "Lucky 13":
            addToScore += 13
        elif currentHand[i] == "Unlucky 7":
            addToScore += 7
        elif currentHand[i] == "The 0":
            temp0Flag = True
    if pMode == 1:
        temp0Flag = False
    if temp0Flag :
        if len(currentHand) < 7 :
            #print("Banked Nothing!")
            total = 0
        else:
            #print("You have " + str(addToScore+pBonus)+" in your hand")
            total = addToScore+15
    else:
        #print("You have " + str(addToScore+pBonus)+" in your hand")
        if len(currentHand) < 7 :
            total = addToScore
        else:
            total = addToScore+15
    return(total)

def Guesstimator(pHandScore):
    global currentHand
    global roundNum
    estimation = pHandScore
    adjustmentConstant = 0.4
    
    if "Lucky 13" in currentHand :
        estimation -= 12
        
    estimation -= (roundNum - 1) * adjustmentConstant
    return(estimation)

print("Round " + str(roundNum))
while score < 200:
    
    #print(ShowProbBust()*100)
    print(Guesstimator(CheckHandScore(1)))
    #choice = input("Please Select: Flip,Bank,ProbBust,ReHand,ReDeal,CheckScore,CheckHand")
    if CheckHandScore() < 27:
        choice = "Flip"
    else:
        choice = "Bank"
    if choice == "Flip":
        if len(masterList) == 0 :
            ReshuffleDeck(currentHand)
            print("Deck Reshuffled!")
            roundNum = 1
        #print(ShowProbBust()*100)
        FlipCard()
        cumulativeProb *= 1 - ShowProbBust()
        
        if CheckBust() :
            roundNum += 1
            ResetHand()
            cumulativeProb = 1.0
            strategyData.append(0)
        if CheckFlip7():
            roundNum += 1
            strategyData.append(CheckHandScore())
            Bank(15)
            ResetHand()
            cumulativeProb = 1.0
        #if len(currentHand) != 0   :
            #print("Your guesstimated chance of busting are: " + str(CheckHandScore()) + "%")
            #print("Your actual chances of busting are: " + str(ShowProbBust()*100) + "%")
            #print("Your old differential is: " + str(CheckHandScore(1) - (ShowProbBust()*100)) + "%")
            #print("My new guestimation is " + str(Guesstimator(CheckHandScore(1))))
            #print("Your new differential is: " + str(Guesstimator(CheckHandScore(1)) - (ShowProbBust()*100)) + "%")
            #heuristicsData.append(Guesstimator(CheckHandScore(1)) - (ShowProbBust()*100))
            
        #else:
        #    roundNum += 1
        #    Bank()
        #    ResetHand()
        #    cumulativeProb = 1.0
       
    elif choice =="Bank":
        roundNum += 1
        strategyData.append(CheckHandScore())
        Bank()
        ResetHand()
        cumulativeProb = 1.0
    #Debug Game Options
    elif choice == "ProbBust":
        ShowProbBust()
    elif choice == "ReHand":
        ResetHand()
    elif choice == "ReDeal":
        ReshuffleDeck(currentHand)
    elif choice == "CheckScore" :
        CheckScore()
    elif choice == "CheckHand" :
        CheckHand()
    elif choice == "ShowData" :
        for i in range(0,len(heuristicsData)):
            print(heuristicsData[i])
            
for i in range(0,len(strategyData)) :   
    print(strategyData[i])
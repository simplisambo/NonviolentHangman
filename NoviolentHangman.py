import time, sys, threading, os, itertools
from threading import Thread
import numpy as np
from random import randint
from termcolor import colored
from getpass import getpass


# Variable declarations

# The 500 most common English words of at least 7 characters
wordBank = ["history", "information", "government", "computer", "reading", "understanding", "literature", "problem", "software", "control", "knowledge", "ability", "economics", "internet", "television", "science", "library", "product", "temperature", "investment", "society", "activity", "industry", "community", "definition", "quality", "development", "language", "management", "variety", "security", "country", "organization", "equipment", "physics", "analysis", "thought", "boyfriend", "direction", "strategy", "technology", "freedom", "environment", "instance", "marketing", "university", "writing", "article", "department", "difference", "audience", "fishing", "marriage", "combination", "failure", "meaning", "medicine", "philosophy", "teacher", "communication", "chemistry", "disease", "advertising", "location", "success", "addition", "apartment", "education", "painting", "politics", "attention", "decision", "property", "shopping", "student", "competition", "distribution", "entertainment", "population", "president", "category", "cigarette", "context", "introduction", "opportunity", "performance", "magazine", "newspaper", "relationship", "teaching", "finding", "message", "appearance", "association", "concept", "customer", "discussion", "housing", "inflation", "insurance", "expression", "importance", "opinion", "payment", "reality", "responsibility", "situation", "statement", "application", "foundation", "grandmother", "perspective", "collection", "depression", "imagination", "passion", "percentage", "resource", "setting", "college", "connection", "criticism", "description", "patience", "secretary", "solution", "administration", "attitude", "director", "personality", "psychology", "recommendation", "response", "selection", "storage", "version", "alcohol", "argument", "complaint", "contract", "emphasis", "highway", "membership", "possession", "preparation", "agreement", "currency", "employment", "engineering", "interaction", "mixture", "preference", "republic", "tradition", "classroom", "delivery", "difficulty", "election", "football", "guidance", "priority", "protection", "suggestion", "tension", "variation", "anxiety", "atmosphere", "awareness", "candidate", "climate", "comparison", "confusion", "construction", "elevator", "emotion", "employee", "employer", "leadership", "manager", "operation", "recording", "transportation", "charity", "disaster", "efficiency", "excitement", "feedback", "homework", "outcome", "permission", "presentation", "promotion", "reflection", "refrigerator", "resolution", "revenue", "session", "cabinet", "childhood", "clothes", "drawing", "hearing", "initiative", "judgment", "measurement", "possibility", "procedure", "relation", "restaurant", "satisfaction", "signature", "significance", "vehicle", "accident", "airport", "appointment", "arrival", "assumption", "baseball", "chapter", "committee", "conversation", "database", "enthusiasm", "explanation", "historian", "hospital", "instruction", "maintenance", "manufacturer", "perception", "presence", "proposal", "reception", "replacement", "revolution", "village", "warning", "assistance", "chocolate", "conclusion", "contribution", "courage", "establishment", "examination", "garbage", "grocery", "impression", "improvement", "independence", "inspection", "inspector", "penalty", "profession", "professor", "quantity", "reaction", "requirement", "supermarket", "weakness", "wedding", "ambition", "analyst", "assignment", "assistant", "bathroom", "bedroom", "birthday", "celebration", "championship", "consequence", "departure", "diamond", "fortune", "friendship", "funeral", "girlfriend", "indication", "intention", "midnight", "negotiation", "obligation", "passenger", "platform", "pollution", "recognition", "reputation", "speaker", "stranger", "surgery", "sympathy", "trainer", "example", "business", "process", "experience", "economy", "interest", "company", "training", "practice", "research", "service", "picture", "exercise", "section", "building", "nothing", "subject", "weather", "beginning", "program", "chicken", "feature", "material", "purpose", "question", "outside", "standard", "exchange", "position", "pressure", "advantage", "benefit", "structure", "account", "discipline", "balance", "machine", "address", "average", "culture", "morning", "condition", "contact", "network", "attempt", "capital", "challenge", "function", "plastic", "influence", "distance", "feeling", "savings", "discount", "officer", "reference", "register", "trouble", "campaign", "character", "evidence", "maximum", "quarter", "background", "strength", "traffic", "vegetable", "kitchen", "principle", "relative", "commission", "minimum", "progress", "project", "breakfast", "confidence", "daughter", "finance", "substance", "afternoon", "consideration", "interview", "mission", "pleasure", "calendar", "contest", "district", "guarantee", "implement", "lecture", "meeting", "parking", "partner", "profile", "respect", "routine", "schedule", "swimming", "telephone", "airline", "designer", "dimension", "emergency", "evening", "extension", "holiday", "husband", "mistake", "mountain", "occasion", "package", "patient", "sentence", "shoulder", "stomach", "tourist", "vacation", "associate", "brother", "document", "landscape", "opening", "pattern", "request", "shelter", "comment", "conference", "monitor", "mortgage", "sandwich", "surprise", "transition", "weekend", "welcome", "bicycle", "concert", "counter", "grandfather", "leather", "pension", "specialist", "champion", "channel", "comfort", "engineer", "entrance", "highlight", "incident", "passage", "promise", "resident", "station", "witness", "general", "specific", "tonight", "possible", "particular", "personal", "current", "national", "natural", "physical", "increase", "individual", "potential", "professional", "international", "alternative", "following", "special", "working", "commercial", "purchase", "primary", "necessary", "positive", "produce", "present", "creative", "support", "complex", "effective", "regular", "reserve", "independent", "original", "beautiful", "negative", "anything", "classic", "private", "western", "concern", "familiar", "official", "comfortable", "valuable", "leading", "release", "display", "objective", "chemical", "extreme", "conflict", "opposite", "deposit", "somewhere"]

global badGuessCount 
global maxBadGuesses
global mistakesLeft
global solveWord
global solveWordArray
global warningsCount

warningsCount = 0
maxBadGuesses = 5
badGuessCount = 0
mistakesLeft = 5
guessCount = 0
previousGuesses = []
playing = False
vsHuman = False
userInput = ""

# Define functions
def showProgress():
    global mistakesLeft
    global maxBadGuesses
    global badGuessCount
    mistakesLeft = maxBadGuesses - badGuessCount
    if mistakesLeft == 0:
        lose()
    for i in range(len(solveWordArray)):
        if correctIndeces[i] == True:
            print(solveWordArray[i], end = " ")
        elif solveWordArray[i] == " ":
            print(solveWordArray[i], end=" ")
        else:
            print("_ ", end = "")
    if mistakesLeft > 5:
        print("\n\nYou have " + str(mistakesLeft) + " mistakes left.")
    if mistakesLeft <= 5 and mistakesLeft>1:
        print(colored("\n\nYou have " + str(mistakesLeft) + " mistakes left.", "yellow"))
    elif mistakesLeft == 1:
        print(colored("\n\nYou have " + str(mistakesLeft) + " mistake left.", "red"))
    if guessCount != 0:
        print("\n\nPrevious guesses: " + str(', '.join(previousGuesses)), end="")

def clear():
    os.system('cls')

def buffer():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if playing:
            break
        sys.stdout.write("\rChoosing a word  " + c)
        sys.stdout.flush()
        time.sleep(0.15)
buffer = threading.Thread(target=buffer)


def tryGuess():
    global badGuessCount
    global warningsCount
    if userInput in previousGuesses:
        print(colored("You already guessed that one. Try again.\n","yellow"))
        warningsCount+=1
    elif guessCount!=0 and (len(userInput) > 1 and len(userInput) != len(solveWord) or not userInput.isalpha()):
        print(colored("Please either guess a letter or guess a word that is " + str(len(solveWord)) + " characters long.\n", "yellow"))
        warningsCount+=1
    elif userInput in solveWord and guessCount != 0:
        print(colored("Yep. What next?\n","green"))
        previousGuesses.append(userInput)
    elif guessCount != 0:
        print(colored("Nope! Try again.\n", "red"))
        badGuessCount += 1
        previousGuesses.append(userInput)
    time.sleep(.5)

def chooseDifficulty():
    global maxBadGuesses
    userInput = input("\nDifficulty:\n\n1) " + colored("Easy\t\t(10 mistakes allowed)","green") + "\n2) " + colored("Medium\t(5 mistakes allowed)","yellow") + "\n3) " + colored("Hard\t\t(3 mistakes allowed)", "red") + "\n\nEnter choice: ")
    if str(userInput) == "1":
        maxBadGuesses = 10
    if str(userInput) == "2":
        maxBadGuesses = 5
    if str(userInput) == "3":
        maxBadGuesses = 3

#def inputSolveWord ():
#    while solveWord.isalpha():
#        global solveWord
#        solveWord = getpass("\nWhat is your secret word? (Your text will be hidden as you type. Press ENTER when finished)\n").upper()

#def resetStopwatch():
#    while True:
#        print("Time elapsed: " + str(round(time.time() - startTime, 2)), end="\r")

def win():
    global mistakesLeft
    totalTime = round(time.time() - startTime,1)
    if mistakesLeft == 1:
        print(colored("\n\nCongratulations! The word was " + solveWord + ". You won in " + str(totalTime) + " seconds with " + str(badGuessCount) + " mistake and " + str(warningsCount) + " warnings.\n", "green"))
    elif warningsCount == 1:
        print(colored("\n\nCongratulations! The word was " + solveWord + ". You won in " + str(totalTime) + " seconds with " + str(badGuessCount) + " mistakes and " + str(warningsCount) + " warning.\n", "green"))
    elif mistakesLeft == 1 and warningsCount == 1:
        print(colored("\n\nCongratulations! The word was " + solveWord + ". You won in " + str(totalTime) + " seconds with " + str(badGuessCount) + " mistake and " + str(warningsCount) + " warning.\n", "green"))
    else:
        print(colored("\n\nCongratulations! The word was " + solveWord + ". You won in " + str(totalTime) + " seconds with " + str(badGuessCount) + " mistakes and " + str(warningsCount) + " warnings.\n", "green"))
    sys.exit()

def lose():
    print(colored("\nOuch. That's " + str(badGuessCount) + " out of the " + str(maxBadGuesses) + " mistakes allowed. The word was " + solveWord + ". Better luck next time.\n", "red"))
    sys.exit()

# Play ball...

print("██\\   ██\\  ██████\\  ██\\   ██\\ ██\\    ██\\ ██████\\  ██████\\  ██\\       ████████\\ ██\\   ██\\ ████████\\       ██\\   ██\\  ██████\\  ██\\   ██\\  ██████\\  ██\\      ██\\  ██████\\  ██\\   ██\\ ")
time.sleep(.03)
print("███\\  ██ |██  __██\\ ███\\  ██ |██ |   ██ |\\_██  _|██  __██\\ ██ |      ██  _____|███\\  ██ |\\__██  __|      ██ |  ██ |██  __██\\ ███\\  ██ |██  __██\\ ███\\    ███ |██  __██\\ ███\\  ██ |")
time.sleep(.03)
print("████\\ ██ |██ /  ██ |████\\ ██ |██ |   ██ |  ██ |  ██ /  ██ |██ |      ██ |      ████\\ ██ |   ██ |         ██ |  ██ |██ /  ██ |████\\ ██ |██ /  \\__|████\\  ████ |██ /  ██ |████\\ ██ |")
time.sleep(.03)
print("██ ██\\██ |██ |  ██ |██ ██\\██ |\\██\\  ██  |  ██ |  ██ |  ██ |██ |      █████\\    ██ ██\\██ |   ██ |         ████████ |████████ |██ ██\\██ |██ |████\\ ██\\██\\██ ██ |████████ |██ ██\\██ |")
time.sleep(.03)
print("██ \\████ |██ |  ██ |██ \\████ | \\██\\██  /   ██ |  ██ |  ██ |██ |      ██  __|   ██ \\████ |   ██ |         ██  __██ |██  __██ |██ \\████ |██ |\\_██ |██ \\███  ██ |██  __██ |██ \\████ |")
time.sleep(.03)
print("██ |\\███ |██ |  ██ |██ |\\███ |  \\███  /    ██ |  ██ |  ██ |██ |      ██ |      ██ |\\███ |   ██ |         ██ |  ██ |██ |  ██ |██ |\\███ |██ |  ██ |██ |\\█  /██ |██ |  ██ |██ |\\███ |")
time.sleep(.03)
print("██ | \\██ | ██████  |██ | \\██ |   \\█  /   ██████\\  ██████  |████████\\ ████████\\ ██ | \\██ |   ██ |         ██ |  ██ |██ |  ██ |██ | \\██ |\\██████  |██ | \\_/ ██ |██ |  ██ |██ | \\██ |")
time.sleep(.03)
print("\\__|  \\__| \\______/ \\__|  \\__|    \\_/    \\______| \\______/ \\________|\\________|\\__|  \\__|   \\__|         \\__|  \\__|\\__|  \\__|\\__|  \\__| \\______/ \\__|     \\__|\\__|  \\__|\\__|  \\__|")

while(True):
    userInput = input("\nWould you be interested in a game of nonviolent hangman? (y/n)\n").upper()
    if userInput == "N":
        sys.exit("\nFine.")
    elif userInput != ("Y" or "N"):
        print("Please choose either 'y' or 'n'.\n")   
    else:
        break

#Introduction Section
while(True):
    clear()
    print("Welcome to nonviolent hangman, where we don't hang people for being bad at a spelling.")
    userInput = input("\nWho would you like to play?\n\n1) Computer\n2) Human\n\nEnter choice: ")
    if str(userInput) == "1":
        solveWord = wordBank[randint(0,499)].upper()
        solveWordArray = list(solveWord.upper())
        correctIndeces = np.full(len(solveWord), False)
        chooseDifficulty()
        buffer.start()
        time.sleep(2)
        playing = True
        break
    elif str(userInput) == "2": 
        solveWord = getpass("\nWhat is your secret word? (Your text will be hidden as you type. Press ENTER when finished)\n").upper()
        solveWordArray = list(solveWord.upper())
        correctIndeces = np.full(len(solveWord), False)
        chooseDifficulty()
        playing = True
        break
    else:
        print("\nPlease choose either 1 or 2.")
        time.sleep(1.5)

startTime = time.time()

#Start Game
while playing and mistakesLeft > 0:
    time.sleep(.5)
    clear()
    tryGuess()
#    resetStopwatch()
    showProgress()
    # Asking user for letter
    userInput = input("\n\nGuess a letter or guess the word:\n").upper()
    guessCount+=1

    # Test if input letter is in word, then adjusting tracker array
    if len(userInput) == 1:
        for i in range(len(solveWordArray)):
            if solveWordArray[i] == userInput:
                correctIndeces[i] = True
    elif userInput == solveWord:
        win()

    if all(correctIndeces):
        win()

lose()

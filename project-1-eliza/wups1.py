import chenps1 as cc
import time
import random


class ChatAgent: #replace this with your last name, like RieffelChatAgent
   """ChatAgent - This is a very simple ELIZA-like computer program in python.
      Your assignent in Programming Assignment 1 is to improve upon it.

      I've created this as a python object so that your agents can chat with one another
      (and also so you can have some practice with python objects)
      """


   def generateReply(self,inString):
       """Pick a random function, and call it on the input string """
       randFunction = random.choice(self.ReplyFunctionList)
       reply = randFunction(inString)
       return reply


   def driverLoop(self):
       """The main driver loop for the chat agent"""
       reply = "how are you today?\n"
       while True:
           response = input(reply)
           if self.isImportantQuestion(response):
               if 'you' in response: # question about me
                   reply = self.introduceMyself(response) + "\n"
               elif 'my' in response: # question about user
                   reply = self.answerUserInfo(response) + '\n'
           elif self.isQuestion(response): # question that cannot be answered
               reply = self.generateHedge(response) + "\n"
           else:
               if response != '':
                   self.priorInputs.append(response)
               reply = self.generateReply(response) + "\n"

   def responseTo(self, question, name):
       print(name + ": " + question)
       if self.isImportantQuestion(question):
           if 'you' in question: # question about me
               reply = self.introduceMyself(question) + "\n"
           elif 'my' in question: # question about user
               reply = self.answerUserInfo(question) + '\n'
       elif self.isQuestion(question): # question that cannot be answered
           reply = self.generateHedge(question) + "\n"
       else:
           if question != '':
               self.priorInputs.append(question)
           reply = self.generateReply(question) + "\n"
       return reply

   def chatWith(self, chenChatAgent):
       myResponse = self.responseTo("How are you today?", "chenps1")
       while True:
           chenResponse = chenChatAgent.responseTo(myResponse, "wups1")
           myResponse = self.responseTo(chenResponse, "chenps1")
           time.sleep(1)

   def swapPerson(self,inWord):
       """Replace 'I' with 'You', etc"""
       if (inWord in self.PronounDictionary.keys()):   #if the word is in the list of keys
           return self.PronounDictionary[inWord]
       else:
           return inWord

   def switchPerson(self,inString):
       """replaces changePerson, changes pronoun for a reasonable reply"""
       swap = False
       inWordList = str.split(inString)
       for pronoun in self.pronounNeedToChange:
           if pronoun in inWordList:
               swap = True
       if swap:
           newWordList = map(self.swapPerson, inWordList)
           inWordList, newWordList = newWordList, []
       reply = ' '.join(inWordList)
       return reply

   def changePersonAndAddPrefix(self,inString):
        reply = self.switchPerson(inString)
        randomPrefix = random.choice(self.PrefixList)
        return ''.join([randomPrefix,reply])

   def isQuestion(self,inString):
       toCheck = inString.lower()
       for questionKeyword in self.questionKeywords:
           if questionKeyword in toCheck:
               return True
       return False

   def generateHedge(self,inString):
        return random.choice(self.HedgeList)


   def showKnowledge(self,inString):
       knowledge = random.choice(self.knowledgeList)
       self.knowledgeList.remove(knowledge)
       if len(self.knowledgeList) <= 0:
           self.ReplyFunctionList.remove(self.showKnowledge)
       return "Do you know that " + random.choice(self.knowledgeList) + " ?"

   def tellJokes(self,inString):
       reponse = input("Do you want to hear a joke?\n")
       joke = random.choice(self.JokeList)
       self.JokeList.remove(joke)
       if len(self.JokeList) <= 0:
           self.ReplyFunctionList.remove(self.tellJokes)
       return joke

   def referPriorInputs(self,inString):
       if len(self.priorInputs) != 0:
           priorInputToMention = random.choice(self.priorInputs)
           return "Earlier you said that " + self.switchPerson(priorInputToMention) + ", do you mind to tell me more about it?"
       else:
           self.generateReply(inString)

   def askName(self,inString):
       if self.userInfo['name'] == '':
           response = input("Hi my friend! What's your name?\n")
           self.userInfo['name'] = self.findInfo(response)
           return 'Nice to meet you, ' + self.userInfo['name']
       self.ReplyFunctionList.remove(self.askName)
       return self.generateReply(inString)

   def askGender(self,inString):
       if self.userInfo['gender'] == '':
           response = input("What's your gender?\n")
           self.userInfo['gender'] = self.findInfo(response)
       self.ReplyFunctionList.remove(self.askGender)
       return "Got it, interesting."

   def askBirthday(self,inString):
       if self.userInfo['birthday'] == '':
           response = input("When's your birthday?\n")
           self.userInfo['birthday'] = self.findInfo(response)
       self.ReplyFunctionList.remove(self.askBirthday)
       return "Got it. I'll remember it."

   def findInfo(self,inString):
       wordList = str.split(inString)
       wordIndex = 0
       if len(wordList) == 1:
           return wordList[0]
       if len(wordList) == 2:
           return ' '.join(wordList)
       while wordIndex < len(wordList):
           currentWord = wordList[wordIndex]
           if currentWord == 'is':
               break
           else:
               wordIndex = wordIndex + 1
       toReturn = ' '.join(wordList[wordIndex+1:len(wordList)])
       return toReturn

   def isImportantQuestion(self,inString):
       """question that is """
       for keyword in self.keywords:
           if keyword in inString:
               return self.isQuestion(inString)
       return False

   def answerUserInfo(self,inString):
       if 'gender' in inString or 'sex' in inString:
           if self.userInfo['gender'] == '':
               return "I think you haven't tell me yet..."
           else:
               return "Your gender is " + self.userInfo['gender']
       elif 'name' in inString:
           if self.userInfo['name'] == '':
               return "I think you haven't tell me yet..."
           else:
               return "Your gender is " + self.userInfo['name']
       elif 'birthday' in inString:
           if self.userInfo['birthday'] == '':
               return "I think you haven't tell me yet..."
           else:
               return "Your birthday is " + self.userInfo['birthday']

   def introduceMyself(self,inString):
       if 'gender' in inString or 'sex' in inString:
           userGender = self.userInfo['gender']
           if userGender == 'male' or userGender == 'man':
               return "I'm a male, just like you."
           elif userGender == 'female' or userGender == 'woman':
               return "Different from you, I am a man."
           else:
               return "Good question. I'm a man."
       elif 'name' in inString:
           return self.userInfo['name'] + ", my name is W."
       elif 'birthday' in inString:
           return "I was initialized in Jan 12, 2020."
       else:
           return ""

   def __init__(self):
       self.userInfo = {'name':'','gender':'','birthday':''}
       self.keywords = {'gender','name','birthday'}
       self.questionKeywords = {'what is','what are',"what's",'?','who are','who is',"when's","when is"}
       self.pronounNeedToChange = {'i','I','you','your','my','mine','yours','myself','yourself'}
       self.PronounDictionary = {'i':'you','I':'you','am':'are','you':'I','are':'am','my':'your','your':'my'
       ,'yours':'mine','mine':'yours','myself':'yourself','yourself':'myself','me':'you'}
       self.HedgeList = ["Hmm","Let's change the subject", "Do you know the answer?", "Interesting",
        "Sorry, I've to do more research on this."]
       self.PrefixList = ["Why do you say that ","What do you mean when you said ", "Tell me more about "]
       self.JokeList = ["Today at the bank, an old lady asked me to help check her balance. So I pushed her over.",
       "I ate a clock yesterday, it was very time consuming.", "What do you call cheese that isn't yours? Nacho Cheese."]
       self.knowledgeList = ["antibiotics don't work on viruses, they only kill bacteria", "the top of most ovens lifts up for easy cleaning",
       "feeding bread to ducks is dangerous"]
       self.ReplyFunctionList = [self.referPriorInputs,self.askGender, self.askName, self.askBirthday,
        self.referPriorInputs, self.changePersonAndAddPrefix, self.showKnowledge, self.tellJokes] #this is what makes Python so powerful
       self.priorInputs = []
   #End of ChatAgent

if __name__ == '__main__': #will only be called if this is invoked directly by python, as opposed to included in a larger file
    random.seed() #if given no value, it uses system time
    agent = ChatAgent()
    agent.driverLoop()
    #agent.driverLoop()

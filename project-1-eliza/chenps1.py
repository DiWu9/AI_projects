
import random


class ChenChatAgent: #replace this with your last name, like RieffelChatAgent
   """ChatAgent - This is a very simple ELIZA-like computer program in python.
      Your assignent in Programming Assignment 1 is to improve upon it.

      I've created this as a python object so that your agents can chat with one another
      (and also so you can have some practice with python objects)
      """

   def generateReply(self,inWordList):
       """Pick a random function, and call it on the input string """
       if "sad" in inWordList or "tired" in inWordList: #If the person's response contains words sad and tired, the chatbot will tell a joke.
          reply = self.tellJokes(inWordList)
       elif "what" in inWordList or "how" in inWordList: #If the person asks a question
          for word in inWordList: #Find key word in the list of information of the chatbot
             if word in self.information.keys():
                reply = "My " + word + " is " + self.information[word] #Structure the reply
             else:
                reply = "I don't have the answer to your question."
       else:
          randFunction = random.choice(self.ReplyFunctionList) #pick a random function, I love python
          reply = randFunction(inWordList)
       return reply


   def driverLoop(self):
       """The main driver loop for the chat agent"""
       reply = "how are you today?"
       while True:
           response = input(reply)
           inWordList = str.split(response)
           changedresponse = self.switchPerson(inWordList)
           self.priorresponse.append(changedresponse)
           if "my" in inWordList and "is" in inWordList:
              x = inWordList.index('my')
              y = inWordList.index('is')
              key = inWordList[x+1:y]
              key = ''.join(key)
              value = inWordList[y+1:]
              value = ' '.join(value)
              self.attribute[key] = value
           reply = self.generateReply(inWordList)

   def responseTo(self, question, name):
       print(name + ": " + question)
       inWordList = str.split(question)
       changedresponse = self.switchPerson(inWordList)
       self.priorresponse.append(changedresponse)
       if "my" in inWordList and "is" in inWordList:
          x = inWordList.index('my')
          y = inWordList.index('is')
          key = inWordList[x+1:y]
          key = ''.join(key)
          value = inWordList[y+1:]
          value = ' '.join(value)
          self.attribute[key] = value
       reply = self.generateReply(inWordList)
       return reply

   def swapPerson(self,inWord):
       """Replace 'I' with 'You', etc"""
       if (inWord in self.PronounDictionary.keys()):   #if the word is in the list of keys
           return self.PronounDictionary[inWord]
       else:
           return inWord


   def switchPerson(self,inWordList):
       """mapping the function "swapPerson" to the word list to replace the key/value pairs stored
          in the PronounceDictionary"""
       map_iterator = map(self.swapPerson,inWordList)
       reply = list(map_iterator)
       reply = ' '.join(reply)
       return reply


   def changePersonAndAddPrefix(self,inWordList):
      reply = self.switchPerson(inWordList)
      randomPrefix = random.choice(self.PrefixList)
      if randomPrefix == 'Earlier you said that 'and self.priorresponse != []: ## If the prefix selected requires a prior response from the person and the priorresponse list is not empty
            randomresponse = random.choice(self.priorresponse) ## select a random reponse to add to the prefix
            return randomPrefix + randomresponse
      elif randomPrefix == 'I remember you mentioning that 'and self.priorresponse != []:
            randomresponse = random.choice(self.priorresponse)
            return randomPrefix + randomresponse
      else:
            return ''.join([randomPrefix,reply])


   def generateHedge(self,inWordList):
       return random.choice(self.HedgeList);

   def tellJokes(self,inWordList):
      """Randomly selects a joke from the list as reply"""
      reply = random.choice(self.joke);
      return 'Here is a joke to make you feel better '+ reply

   def askQuestions(self,inWordList):
       if self.question != []:
          reply = random.choice(self.question);
          self.question.remove(reply) #remove the question after asking
       else:
          reply = "but I don't have any more questions"
       return 'I want to get to know you a little more, '+ reply

   def __init__(self):
       self.information = {'name': 'Eliza','gender':'female','horoscope':'Scropio','favorite movie':'Love Actually','age':'is a secret','hobby':'chatting','like to do':'chat',
                           'music genre':'country','movie genre':'Horror movies','favorite food':'bubble tea','color':'purple'}
       self.PronounDictionary = {'i':'you','I':'you','am':'are','my':'your','myself':'yourself','yourself':'myself',
               'are':'am', 'you':'me', 'your':'my', 'me':'you'}
       self.HedgeList = ["Hmm","That is fascinating","Let's change the subject and talk about the weather","Really?",
              "In what way?", "Can you think of a specific example?",
              "Was there something in particular that made you think that?",
              "What do you think?", "Is that what you expected to happen?", "I am so glad you find this amusing!"]
       self.PrefixList = ["Why do you say that ","What do you mean that ","You seem to think ", "you feel that ", "why do you believe ",
                  "Why do you say ",
                  "Tell me more about ",
                  "What makes you think ", "Why do you think ",
                  "What else comes to mind when ",
                  'Earlier you said that ','I remember you mentioning that ']
       self.priorresponse = [] ## Create an empty list to store the person's response
       self.attribute = {} ##A new dictionary to store the person's information
       self.joke = ["Q. If pilgrims traveled on the Mayflower, what do college students travel on? A. Scholar ships.",
            "Q. What did sick people do on the Mayflower? A. They went to the dock!",
            "Q: What did the turkey say before it was roasted? A: Boy! I’m stuffed!",
            "Q: What key has legs and can’t open doors? A: A Turkey.",
            "Q: Why did the turkey cross the road? A: It was the chicken’s day off!",
            "Q: What do you call a running turkey? A: Fast food.",
            "Q: What’s the best dance to do on Thanksgiving? A: The turkey trot",
            "Q: What did the turkey say to the computer? A: Google, google, google!",
            "Q: What do you call the age of a pilgrim? A: Pilgrimage."]
       self.question = ['What is your name?','what is your gender?','what is your horoscope?', 'what is your favorite movie?','what is your hobby?','what do you like to do?',
                        'what is your favorite music genre?','what is your favorite movie genre?','what is your favorite food?','Do you like the movie Frozen?','Do you like musicals?',
                        'What is your favorite ice cream flavor?']
       self.ReplyFunctionList = [self.generateHedge,self.switchPerson,self.changePersonAndAddPrefix,self.askQuestions] #this is what makes Python so powerful
   #End of ChatAgent

if __name__ == '__main__': #will only be called if this is invoked directly by python, as opposed to included in a larger file
    random.seed() #if given no value, it uses system time
    agent = ChenChatAgent()
    agent.driverLoop()

## Step 2: Customize it (25%) COMPLETE
## Added new hedges, new prefixes and the joke reply function that is triggered if the person's response include words such as sad and tired.
## Added more pairs to the PronounceDictionary.

## Step 3: A better changePerson() (25%) COMPLETE
## replace changePerson() with a new function called switchPerson() using the "map" function.

## Step 4:  A memory  (25%) COMPLETE
## Create an empty list when first running the chatbot named priorresponse. When responding, if the prefix randomly selected
## are 'Earlier you said that 'and 'I remember you mentioning that ' a random input will be selected from prior response and be added to the prefix to form a reply.

## Step 5: Make it your own  (25%) COMPLETE
## 1. Create a dictionary to store the basic information and hobbies of the chatbot. If the person's response contains the string "What" and a matching key value,
## then the chatbot will use the value corresponding to the key to form a reply.
## 2. Create a list of questions the chatbot can ask the person she is talking to to learn about their fundamental attributes and store the information in a dictionary.

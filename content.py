# Define what content is generated and/or consumed inside the network
import random
import numpy as np
from agent import Agent

class Content:
    allContent = []
    def __init__(self):
        self.id = Content.generateUniqueID(self)
        self.type = None
        self.origMsg = None # ID of original variant of message
        self.IsItTrue = True
        self.processload = None
        self.timeNeeded = None
        self.apparentSource = None # what source it represents to come from, None if anonymous
        self.actualSource = None # internal variable that keeps track of true origin (original author)
        self.sender = None # ID of person who last sent the message, anonymous if not known
        self.positivity = None
        self.interesting = None
        self.controversy = None
        self.professionalism = None
        self.emotionalImpact = None
        self.impactDirection = 1 # tuple with issue and modifier
        self.socialValue = 0
        self.factLevel = None
        self.triggerRate = 0.5
        self.callToAction = False
        self.initializeMsg()
        # self.virality = 1 # virality #for testing purposes put at 1
        Content.allContent.append(self)

    def initializeMsg(self):
        # things that are predetermined
        self.origMsg = self
        try:
            custom = int(input("Would you like to \n1. set the parameters for the content \n2. to auto-generate? \n"))
            if custom != 1 and custom != 2:
                raise ValueError
        except ValueError:
            print("Invalid input. Generating a random message.")
            custom = 2
        if custom == 1:
            # type of message: informative, persuasive, entertainment
            self.type = random.randint(1, 3)
            #true or not
            if random.randint(0, 1) == 0:
                self.IsItTrue = False
            else:
                self.IsItTrue = True
            # time needed in seconds
            self.timeNeeded = np.random.normal(120, 60)
        else:
            #set type
            try:
                self.type = int(input("Is this message primarily 1. informative, 2. persuasive, 3. for entertainment? "))
                if self.type < 0 or self.type > 3:
                    raise ValueError
            except ValueError:
                print("Invalid input. Setting as default: informative.")
                self.type = 1
            # true or not
            self.IsItTrue = input("Is this message 1. True or 2. False? ")
            if self.IsItTrue == '1':
                self.IsItTrue = True
            elif self.IsItTrue == '2':
                self.IsItTrue = False
            else:
                print("Invalid option. Setting as true.")
                self.IsItTrue = True
            # time needed in seconds
            try:
                self.timeNeeded = int(input("How many seconds would someone typically need to read/watch this content?"))
                if self.timeNeeded < 0:
                    raise ValueError
            except ValueError:
                print("Invalid input. Setting as default: 120 seconds.")
                self.timeNeeded = 120
            # who is the actual source
            try:
                src = int(input("What kind of agent should be selected to send the message? \n1. media \n2. bot \n3. normal"))
                if src < 0 or src > 3:
                    raise ValueError
            except ValueError:
                print("Invalid input. Setting as default: media.")
                src = 1
            finally:
                self.actualSource = Content.getRandomSource(src)
            # who is the apparent source            
            try:
                src = int(input("Who is the apparent source of this content? \n1. Anonymous \n2. Actual Source \n3. Pretend to be Another (not available for media, factcheckers))"))
                if (src > 3 or src < 0):
                    raise ValueError
                elif src == 3 and (self.actualSource.type == 'media' or self.actualSource.type == 'factchecker'):
                    raise ValueError
            except ValueError:
                print("Invalid value. Selecting Actual Source as default.")
                src = 2
            finally:
                if src == 1:
                    self.apparentSource = None
                elif src == 2:
                    self.apparentSource = self.actualSource    
                elif src == 3:
                    src = int(input("What type of media source should it try to spoof? \n1. One of the most followed accounts. \n2. An account with a particular political reputation. "))
                    try:
                        if src == 1 or src ==2:
                            self.apparentSource = Content.getRandomSource(src+3)
                        else:
                            raise ValueError
                    except ValueError:
                        print("Invalid input. Setting a random popular media agent as the source.")
                        self.apparentSource = Content.getRandomSource(4)
                else:
                    self.apparentSource = self.actualSource
            # apparent sender
            self.sender = self.apparentSource
            # how positive the message is        
            self.positivity = None
        
        '''
        self.positivity = None
        self.interesting = None
        self.controversy = None
        self.professionalism = None
        self.emotionalImpact = None
        self.impactDirection = 1 # tuple with issue and modifier
        self.socialValue = 0
        self.factLevel = None
        self.triggerRate = 0.5
        self.callToAction = False'''
        #self.processload = None
            try:
                self.type = int(input("Choose a type of message: \n1. Informative \n2. Persuasive \n3. Entertainment"))
                if self.type > 3 or self.type <1:
                    raise ValueError
            except ValueError:
                print("That is not an available type. The message will be informative by default.")
    
    @staticmethod
    def getRandomSource(option):
        if option == 1:
            if len(Agent.allMedia) < 1:
                print("No media sources. Choosing a source at random.")
                return random.choice(Agent.allAgents)
            return random.choice(Agent.allMedia)
        elif option == 2:
            if len(Agent.allBots) < 1:
                print("No bots. Choosing a source at random.")
                return random.choice(Agent.allAgents)
            return random.choice(Agent.allBots)
        elif option == 3:
            if len(Agent.allNormies) < 1:
                print("No normal accounts. Choosing a source at random.")
                return random.choice(Agent.allAgents)
            return random.choice(Agent.allNormies)
        elif option == 4:
            numChoices = int(len(Agent.allMedia)*0.3) # always choose to spoof from amongst the most well-connected accounts
            if numChoices > 0:
                i = random.randint(0, numChoices-1)
                return Agent.allMedia[i]
            else:
                print("No media sources. Choosing a source at random.")
                return random.choice(Agent.allAgents)
        elif option == 5:
            try:
                spoofNum = int(input("About where is political alignment level of the media source the bot will select for spoofing?"))
                if (spoofNum > 100 or spoofNum < 0):
                    raise ValueError
            except ValueError:
                print("Value is invalid... Randomly choosing a more politically left or right source to spoof.")
                spoofNum = random.randint(0, 1)*100
                sortedByExtreme = sorted(Agent.allMedia, key=lambda agent: (agent.politBias - spoofNum))
                return sortedByExtreme[0]
        else:
            return random.choice(Agent.allAgents)
    
    def evolveMsg(self):
        pass # don't forget to make a copy rather than modifying the orig message
    
    def generateUniqueID(self):
        checkid = 0
        while True:
            found = False
            for item in Content.allContent:
                if item.id == checkid:
                    found = True
                    checkid+=1
                    break
            if found == False:
                return checkid
            
if __name__ == "__main__":
    contents = []
    for i in range(10):
        contents.append(Content(1))
    print("All Contents")
    for con in contents:
        print(con.id)
    
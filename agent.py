from issue import Issue
from content import Content
from network1 import Node
import random
import math
import numpy as np

class Agent(Node):
    allAgents = []
    allMedia = []
    allBots = []
    allCheckers = []
    allNormies = []
    def __init__(self, id: int):
        super().__init__(id)
        self.type = None
        #demographic
        self.gender = None
        self.age = None
        #personality
        self.neurotic = None
        self.open = None
        self.conscientious = None
        self.agreeable = None
        self.extravert = None
        self.empathy = None
        self.narcissist = None
        self.manipulative = None
        #ability
        self.edu = None
        self.emotionreg = None
        self.analytic = None
        self.emointel = None
        self.impulsive = None
        #biases
        self.groupAff = None
        self.affDepend = None
        self.politbias = None
        self.beliefPersist = None #suspicious of new beliefs?
        self.prefConsist = None
        #habits
        self.attention = None
        self.timeOnInternet = None
        #current state
        self.personalUtility = 0
        self.listContentKnown = []
        self.issueList = []
        self.sourceList = []
        
    def __str__(self):
        str = f"Agent {self.id} is a {self.type} account that has the following traits: "
        if self.type == 'normal':
            str += f"\nNeurotic = {self.neurotic} \nOpen = {self.open} \nConscientious = {self.conscientious} \nAgreeable = {self.agreeable} \nExtravert = {self.extravert}"
            str += f"\nEmotional Control = {self.emotionreg} \nNarcissist = {self.narcissist}"
            str += f"\nManipulativeness = {self.manipulative} \nEmpathy = {self.empathy} \nEmotional Intelligence = {self.emointel}"
            str += f"\nImpulsiveness = {self.impulsive} \nDependence on Affirmation = {self.affDepend}"
            str += f"\nEmotional Control = {self.emotionreg} \nYears of Education = {self.emotionreg}"
            str += f"\nAnalytical Ability = {self.analytic} \nAttention Span in Seconds = {self.attention}"
            str += f"\nTime on Internet in Hours = {self.timeOnInternet}"
        str += f"\nPolitical Leaning = {self.politBias} \nGroup Affinity = {self.groupAff}"
        str += f"\nBelief Persistence = {self.beliefPersist} \nPreference for Consistency = {self.prefConsist} \n\n"
        for source in self.sourceList:
            str += f"\nThis agent has an opinion score of {source[2]} and friend score of {source[1]} with {source[0].id}."
        for issue in self.issueList:
            str += f"\nThis agent has an opinion {issue[1]} on the issue of {issue[0].issueName}."
        return str
    
    @staticmethod
    def generate0_100(avg, std):
        num = 0
        while (num <= 0 or num >= 100):
            num = math.floor(np.random.normal(avg, std))
        return num
    
    @staticmethod
    def generateSkewedOld(self):
        asym =0
        meanAge = 50
        std = 10
        scale = 15
        while asym < 18 or asym > 90:
            normalPart = np.random.normal(meanAge, std)
            expPart = np.random.exponential(scale)
            asym = int(normalPart + expPart)
        return asym
    
    @staticmethod
    def initializeAgents():
        Agent.allAgents.sort(key=lambda agent: len(agent.connected))
        # population characteristics
        try:
            mediaPr = int(input("About what percent of agents are mass media? 0 to 100: "))
            if mediaPr > 100 or mediaPr < 0:
                mediaPr = 10
                raise ValueError
            botPr = int(input("About what percent of agents are bots? 0 to 100: "))
            if (botPr+mediaPr) > 100 or botPr < 0:
                botPr = 5
                raise ValueError
            factPr = int(input("About what percent of agents are factcheckers? 0 to 100: "))
            if (factPr+botPr+mediaPr) > 100 or factPr < 0:
                factPr = 1
                raise ValueError
        except ValueError:
            mediaPr = 10
            botPr = 5
            factPr = 1
            print(f"Invalid response. \nAfter setting defaults, {mediaPr}% media, {botPr}% bots, {factPr}% factcheckers, rest normal.")
        try:
            popDist = int(input("What is the population's age distribution? 1. older, 2. younger, 3. uniform \n"))
            if popDist > 3 or popDist < 1:
                raise ValueError
        except ValueError:
            print("Invalid response. Setting to uniform")
            popDist = 3
        try:
            bigFive = input("Would you like to define the personality tendencies of the culture group? Y/N ")
            if bigFive.upper() == 'Y':
                try:
                    neu = input("About where is the average neuroticism level (between 1 and 100), 50 being default. ")
                    if (neu > 100 or neu < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    neu = 50
                try:
                    open = input("About where is the average openness level (between 1 and 100), 50 being default. ")
                    if (open > 100 or open < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    open = 50
                try:
                    cons = input("About where is the average conscientiousness level (between 1 and 100), 50 being default. ")
                    if (cons > 100 or cons < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    cons = 50
                try:
                    agr = input("About where is the average agreeableness level (between 1 and 100), 50 being default. ")
                    if (agr > 100 or agr < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    agr = 50
                try:
                    extr = input("About where is the average extraversion level (between 1 and 100), 50 being default. ")
                    if (extr > 100 or extr < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    extr = 50
                try:
                    emp = input("About where is the average empathy level (between 1 and 100), 50 being default. ")
                    if (emp > 100 or emp < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    emp = 50
                try:
                    nar = input("About where is the average narcissism level (between 1 and 100), 20 being default. ")
                    if (nar > 100 or nar < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    nar = 20
                try:
                    manip = input("About where is the average manipulativeness level (between 1 and 100), 20 being default. ")
                    if (manip > 100 or manip < 0):
                        raise ValueError
                except ValueError:
                    print("Value is invalid. Setting default to 50.")
                    manip = 20
            elif bigFive.upper() == 'N':
                neu = 50
                open = 50
                cons = 50
                agr = 50
                extr = 50
                emp = 50
                extr = 50
                emp = 50
                nar = 20
                manip = 20
            elif bigFive.upper() != 'N':
                raise ValueError    
        except ValueError:
            print("Invalid response. Will randomly generate personality characteristics.")                
            neu = 50
            open = 50
            cons = 50
            agr = 50
            extr = 50
            emp = 50
            extr = 50
            emp = 50
            nar = 20
            manip = 20
        try:
            edu = int(input("How many years of education does a typical person in this community have? "))
            if (edu < 0 or edu > 20):
                raise ValueError
        except ValueError:
            print("Value entered is invalid. Setting 9 as default.")
            edu = 9
        try:
            politicalDivision = int(input("How divided is the world we are living in? (between 0 and 100, default=33): "))
            if (politicalDivision < 0 or politicalDivision > 100):
                raise ValueError
        except ValueError:
            print("\nValue entered is invalid. Setting value at 33.")
            politicalDivision = 33
        try:
            meanPoliticalView = int(input("What is an average person's political inclination between 0 and 100? (50 for neutral): "))
            if (meanPoliticalView < 0 or meanPoliticalView > 100):
                raise ValueError
        except ValueError:
            print("\nValue entered is invalid. Setting value at 50.")
            meanPoliticalView = 50
        try:
            grpThink = int(input("On average, how much group affinity matter (as opposed to individualism), on a scale of 0 to 100? "))
            if (grpThink < 0 or grpThink > 100):
                raise ValueError
        except ValueError:
            print("\nValue entered is invalid. Setting value at 50.")
            grpThink = 50
        try:
            insular = int(input("In this society, are friendships \n1. Found anywhere (randomize) or \n2. Clustered on mutual social ties? \n"))
            if (insular != 1 and insular != 2):
                raise ValueError
        except ValueError:
            print("\nValue entered is invalid. Setting values at random.")
            insular = 1
        try:
            dist = int(input("Would you like the population to \n1. start neutral \n2. start with anticipated distributions of issue opinion? "))
            if (dist < 1 or dist > 2):
                raise ValueError
        except ValueError:
            print("\nValue entered is invalid. Setting according to anticipated distributions.")
            dist = 2
        # set individual values based on population characteristics, distributions
        for a in Agent.allAgents:
            # set type
            if random.randint(0, 100) < mediaPr:
                a.type = "media"
                Agent.allMedia.append(a)
            elif random.randint(0, 100) < mediaPr + botPr:
                a.type = "bot"
                Agent.allBots.append(a)
            elif random.randint(0, 100) < mediaPr + botPr + factPr:
                a.type = "factchecker"
                Agent.allBots.append(a)
            else:
                a.type = "normal"
                Agent.allNormies.append(a)
            if a.type == 'normal':
                # set gender
                gen = random.randint(0, 1)
                if gen == 0:
                    a.gender = 'M'
                else:
                    a.gender = 'F'
                # set age
                if popDist == '1':
                    age = int(np.random.exponential(72)) # 0 to around 72 but not hard ceiling
                    while (age > 72):
                        age = int(np.random.exponential(72))
                    a.age = age +18
                if popDist == '2':
                    a.age = Agent.generateSkewedOld()
                else:
                    a.age = int(random.uniform(18, 90))
                # set personality characteristics
                a.neurotic = Agent.generate0_100(neu, 33)
                a.open = Agent.generate0_100(open, 33)
                a.conscientious = Agent.generate0_100(cons, 33)
                a.agreeable = Agent.generate0_100(agr, 33)
                a.extravert = Agent.generate0_100(extr, 33)
                a.narcissist = Agent.generate0_100(nar, 20)
                a.manipulative = Agent.generate0_100(manip, 20)
                a.empathy = Agent.generate0_100(emp, 33)
                a.emointel = Agent.generate0_100(50, 33)
                a.impulsive = Agent.generate0_100(50, 33)
                a.affDepend = Agent.generate0_100(50, 33)
                # set ability characteristics
                a.emotionreg = Agent.generate0_100(50, 33)
                a.edu = int(np.random.normal(edu, 3))
                while (a.edu < 0 or a.edu > 20):
                    a.edu = int(np.random.normal(edu, 3))
                a.analytic = Agent.generate0_100(50, 33)
                a.attention = int(np.random.normal(20, 10))
                while (a.attention < 3):
                    a.attention = int(np.random.normal(20, 10))
                a.timeOnInternet = int(np.random.normal(3, 10))
                while (a.timeOnInternet < 0 or a.timeOnInternet > 24):
                    a.timeOnInternet = int(np.random.normal(3, 10))
            # characteristics that all types of agents have
            a.politBias = int(np.random.normal(meanPoliticalView, politicalDivision))
            while (a.politBias < 0 or a.politBias > 100):
                a.politBias = int(np.random.normal(meanPoliticalView, politicalDivision))
            a.groupAff = int(np.random.normal(grpThink, 33))
            while (a.groupAff < 0 or a.groupAff > 100):
                a.groupAff = int(np.random.normal(grpThink, 33))
            if a.type == 'normal':
                a.beliefPersist = int(np.random.normal(100-a.open/2, 20))
                while a.beliefPersist < 10 or a.beliefPersist > 90:
                    a.beliefPersist = int(np.random.normal(100-a.open/2, 20))
            else:
                a.beliefPersist = int(np.random.normal(50, 33))
                while a.beliefPersist < 10 or a.beliefPersist > 90:
                    a.beliefPersist = int(np.random.normal(50, 33))
            a.prefConsist = int(np.random.normal(50, 33))
        Agent.allMedia.sort(key=lambda media: len(media.connected))
        Agent.allBots.sort(key=lambda bot: len(bot.connected))
        Agent.allCheckers.sort(key=lambda checker: len(checker.connected))
        # after initializing baseline traits for all agents, establish opinions of one another
        for a in Agent.allAgents:
            for other in a.connected:
                if other.type == 'normal':
                    #each known connection has a closeness level and a trustJudgment level
                    fr = random.randint(0, 100)
                    if insular == 2:
                        acq1 = set(a.connected)
                        acq2 = set(other.connected)
                        mutualAcq = len(acq1.intersection(acq2))
                        fr = int(fr+fr*mutualAcq*2/len(a.connected)*a.groupAff/50)
                        if (fr > 100):
                            fr = 100
                    trust = int(random.randint(0, 100)*(1 - abs(a.politBias - other.politBias)/100))
                    a.sourceList.append((other, fr, trust))
                else: # for impersonal sources, such as media, bot, factchecker
                    fr = 0
                    trust = random.randint(0, 100)
                    if dist == 2:
                        trust = 100 - abs(a.politBias - other.politBias)
                    a.sourceList.append((other, fr, trust))
            for i in range(0, len(Issue.allIssues)):
                opinions = Issue.generateIssueOpinions(meanPoliticalView, a.politBias)
                a.issueList.append([Issue.allIssues[i], int(opinions[i])])

    def decide(self, content: Content, broadcastOn=True, nothingOn=True):
        # decide what to do based on content and agent rules + properties
        # for now, spread at probability virality
        whoAffected = [] #automatically updated by reaction functions, each element has format [sender, recipient, content]
        if (random.uniform(0.0, 1.0) < content.virality):
            #based on passing a threshold virality, agent decides to do "something"
            if broadcastOn == False:
                m = 2 #share few
            else:
                m = 1 #broadcast
            if nothingOn == False:
                n = 2
            else:
                n = 3 #do nothing
            reactionSeed = random.randint(m, n) #for testing purposes can do 2, 2. change back to 1, 3 later.
            if (reactionSeed == 1):
                self.broadcastContent(content, whoAffected)
                #print(f"{self.id} broadcasted to: ", end = " ")
            elif (reactionSeed == 2):
                self.shareFew(content, whoAffected)
                #print(f"{self.id} shared with close friends!", end = " ")
            else:
                pass
        '''
        for a in whoAffected:
            print(a[1].id, end=" ")
        print("")
        '''
        return whoAffected
        
    def broadcastContent(self, content, whoAffected):
        for friend in self.connected:
            updateFlag = friend.updateInfo(content)
            if updateFlag:
                whoAffected.append([self, friend, content])
    
    def shareFew(self, content, whoAffected):
        # for now, just random probability, but later, will add proximity/affinity type variables
        p = 0.3
        for friend in self.connected:
            if random.uniform(0.0, 1.0) < p:
              updateFlag = friend.updateInfo(content)
              if updateFlag:  # maybe later create repetition effects
                    whoAffected.append([self, friend, content])
    
    def updateInfo(self, content):
        #checks if info is already known before appending
        if content in self.listContentKnown:
            return False
        else:
            self.listContentKnown.append(content)
            return True
    
    def generate(self):
        # decide what or if to generate content based on agent rules + properties
        content = Content(self, random.uniform(0.0, 1.0))
        self.listContentKnown.append(content)
        return content